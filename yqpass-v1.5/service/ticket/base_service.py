#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date: 2018/8/7 15:45
import datetime
import json
from json import JSONDecodeError

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q, Max

from backend.fielddiy.models import ApplicationDetail
from backend.resmanage.models import BuildingRoomInfo, RouteInfo
from backend.ticket.models import TicketRecord, TicketCustomField, TicketFlowLog
from backend.workflow.models import Transition, CustomField
from service.account.base_services import AccountBaseService
from service.common.base_services import BaseService
from service.common.constant_service import CONSTANT_SERVICE
from service.common.log_service import auto_log
from service.common.permission_check import check_new_ticket_permission, ticket_handle_permission_check, \
    ticket_view_permission_check, admin_permission_check
from service.workflow.base_services import WorkflowBaseService
from service.workflow.custom_field_service import WorkflowCustomFieldService
from service.workflow.state_service import WorkflowStateService
from service.workflow.transition_service import WorkflowTransitionService

__author__ = 'x-zj'


class TicketBaseService(BaseService):
    """
    工单的基础服务
    """

    def __init__(self):
        pass

    @classmethod
    @auto_log
    def get_ticket_list(cls,
                        sn='',
                        title='',
                        username='',
                        workflow_id='',
                        create_start='',
                        create_end='',
                        category='',
                        reverse=1,
                        per_page=10,
                        page=1):
        """
        获取工单列表
        :param sn: 流水单号
        :param title: 标题
        :param username: 用户名
        :param create_start: 从创建时间起
        :param workflow_id:
        :param create_end:
        :param category: 查询类别(创建的，待办的，关联的:包括创建的、处理过的、曾经需要处理但是没有处理的)
        :param reverse: 按照创建时间倒序
        :param per_page: 每页显示个数，默认10
        :param page: 页码，默认1
        :return:
        """
        # 'all':所有工单, 'owner':我创建的工单, 'duty':我的待处理工单, 'relation':我的关联工单[包括我新建的、我处理过的]
        category_list = ['all', 'owner', 'duty', 'relation']
        if category not in category_list:
            return False, "查询类别错误，请重新选择。"

        query_params = Q(is_deleted=0)
        if sn:
            query_params &= Q(sn__startswith=sn)
        if title:
            query_params &= Q(title__contains=title)
        if create_start:
            # create_start = datetime.datetime.strptime(create_start, '%Y-%m-%d %H:%M:%S')
            query_params &= Q(gmt_created__gte=create_start)
        if create_end:
            query_params &= Q(gmt_created__lte=create_end)
        if workflow_id:
            query_params &= Q(workflow_id=workflow_id)

        if reverse:
            order_by_str = '-gmt_created'
        else:
            order_by_str = 'gmt_created'

        if category == 'owner':
            query_params &= Q(creator=username)
            ticket_objects = TicketRecord.objects.filter(
                query_params).order_by(order_by_str)

        elif category == 'duty':
            """
            待办工单, 首先获取用户对象, 取出相关联的部门id和角色id。然后再判断多人的情况怎么处理
            """
            user_obj, msg = AccountBaseService.get_user_by_username(username)
            if not user_obj:
                return False, msg
            user_dept_id_list, msg2 = AccountBaseService.get_user_dept_id_list(
                username)
            user_role_id_list, msg3 = AccountBaseService.get_user_role_id_list(
                username)
            if user_dept_id_list is False:
                return False, msg2
            if user_role_id_list is False:
                return False, msg3
            user_dept_id_str_list = [
                str(user_dept_id) for user_dept_id in user_dept_id_list
            ]
            user_role_id_str_list = [
                str(user_role_id) for user_role_id in user_role_id_list
            ]
            # 个人接单|角色结单|部门结单
            duty_query_expression = Q(
                participant_type_id=CONSTANT_SERVICE.PARTICIPANT_TYPE_PERSONAL,
                participant=username)
            duty_query_expression |= Q(
                participant_type_id=CONSTANT_SERVICE.PARTICIPANT_TYPE_DEPT,
                participant__in=user_dept_id_str_list)
            duty_query_expression |= Q(
                participant_type_id=CONSTANT_SERVICE.PARTICIPANT_TYPE_ROLE,
                participant__in=user_role_id_str_list)

            # 选择多人的情况, 用逗号隔开, 需要用extra查询实现。 会存在注入问题。
            ticket_query_set1 = TicketRecord.objects.filter(
                query_params).extra(where=[
                'FIND_IN_SET("{}", participant)'.format(username),
                'participant_type_id={}'.format(CONSTANT_SERVICE.
                                                PARTICIPANT_TYPE_MULTI)
            ])
            query_params &= duty_query_expression
            ticket_query_set2 = TicketRecord.objects.filter(query_params)
            ticket_objects = (ticket_query_set1
                              | ticket_query_set2).order_by(order_by_str)

        # 关联工单, 因为 relation 字段已经保留了工单的处理人信息, 所以只需要找到哪些工单这个字段中包含该 user 就ok了
        elif category == 'relation':
            ticket_objects = TicketRecord.objects.filter(query_params).extra(
                where=['FIND_IN_SET("{}", relation)'.format(username)
                       ]).order_by(order_by_str)

        else:
            ticket_objects = TicketRecord.objects.filter(
                query_params).order_by(order_by_str)

        paginator = Paginator(ticket_objects, per_page)
        try:
            ticket_result_paginator = paginator.page(page)
        except PageNotAnInteger:
            ticket_result_paginator = paginator.page(1)
        except EmptyPage:
            ticket_result_paginator = paginator.page(paginator.num_pages)

        # 分页后要显示的工单列表
        ticket_result_object_list = ticket_result_paginator.object_list
        ticket_result_restful_list = []

        for ticket_result_object in ticket_result_object_list:
            # 工单状态与处理人信息
            state_obj, msg = WorkflowStateService.get_restful_state_info_by_id(
                ticket_result_object.state_id)
            state_name = state_obj['name']

            participant_info, msg = cls.get_ticket_format_participant_info(
                ticket_result_object.id)
            if participant_info is False:
                return False, msg

            # 所属于工作流信息
            workflow_obj, msg = WorkflowBaseService.get_by_id(
                ticket_result_object.workflow_id)
            workflow_info_dict = dict(
                workflow_id=workflow_obj.id, workflow_name=workflow_obj.name)

            ticket_result_restful_list.append(
                dict(
                    id=ticket_result_object.id,
                    title=ticket_result_object.title,
                    workflow=workflow_info_dict,
                    sn=ticket_result_object.sn,
                    state=dict(
                        state_id=ticket_result_object.state_id,
                        state_name=state_name),
                    parent_ticket_id=ticket_result_object.parent_ticket_id,
                    parent_ticket_state_id=ticket_result_object.
                        parent_ticket_state_id,
                    participant_info=participant_info,
                    creator=ticket_result_object.creator,
                    modifier=ticket_result_object.modifier,
                    application_date=str(
                        ticket_result_object.application_date)[0:10],
                    gmt_created=str(ticket_result_object.gmt_created)[0:19],
                    gmt_modified=str(ticket_result_object.gmt_modified)[0:19],
                ))
        return ticket_result_restful_list, dict(
            per_page=per_page, page=page, total=paginator.count)

    @classmethod
    def new_ticket(cls, request_data_dict):
        """
        新建工单, Post 方式访问, 意味着从 request_data_dict 中获取新建工单的详细字段信息。
        1. 提取该工作流该状态中的必填字段, 校验。
        2. 获取对应工作流的初始状态, 与提供的 request_data_dict 数据进行校验匹配。
        3. 获取下一个流程的状态, 根据状态要求与提供的数据生成一张新的工单
        4. 添加流转记录等信息
        :param request_data_dict:
        :return:
        """
        transition_id = request_data_dict.get('transition_id')
        username = request_data_dict.get('username')
        workflow_id = request_data_dict.get('workflow_id')
        parent_ticket_id = request_data_dict.get('parent_ticket_id', 0)
        parent_ticket_state_id = request_data_dict.get(
            'parent_ticket_state_id', 0)
        suggestion = request_data_dict.get('suggestion', '')
        application_date = request_data_dict.get(
            'application_date',
            str(datetime.datetime.now())[:10])
        if not (workflow_id and transition_id and username):
            return False, "参数不合法, 请提供workflow_id, username, transition_id, title"

        # 提取工单字段列表
        request_field_arg_list = [
            key for key, value in request_data_dict.items()
            if (key not in ['workflow_id', 'suggestion', 'username'])
        ]

        # 判断用户是否有权限新建工单
        has_permission, msg = check_new_ticket_permission(
            username, workflow_id)
        if not has_permission:
            return False, msg

        # 获取工单必填信息
        # 获取工作流初始状态, 校验填写的工单数据
        start_state, msg = WorkflowStateService.get_workflow_start_state(
            workflow_id)
        if not start_state:
            return False, msg

        # 获取初始状态中字段的读写权限
        state_field_dict = json.loads(start_state.state_field_str)
        require_field_list, update_field_list = [], []
        for key, value in state_field_dict.items():
            if value == CONSTANT_SERVICE.FIELD_ATTRIBUTE_REQUIRED:
                require_field_list.append(key)
                update_field_list.append(key)
            if value == CONSTANT_SERVICE.FIELD_ATTRIBUTE_OPTIONAL:
                update_field_list.append(key)

        # 校验是否所有必填项都有提供, 同时如果在 transition_id 对应的流转设置为不校验则直接通过
        req_transition_obj, msg = WorkflowTransitionService.get_workflow_transition_by_id(
            transition_id)
        if not req_transition_obj:
            return False, msg
        if req_transition_obj.field_require_check:
            for require_field in require_field_list:
                if require_field not in request_field_arg_list:
                    return False, "new_ticket: 此工单必填字段为: {}".format(
                        ','.join(require_field_list))

        # 根据 transition_id 获取对应下个状态的信息, 同时校验 request_data_dict 中的流转 id 是否合法。
        transition_queryset, msg = WorkflowTransitionService.get_state_transition_queryset(
            start_state.id)
        if not transition_queryset:
            return False, msg
        allow_transition_id_list = [
            transition.id for transition in transition_queryset
        ]

        if transition_id not in allow_transition_id_list:
            return False, "transition_id 不合法, 请提供正确的 transition_id"

        destination_state_obj = Transition.objects.filter(
            id=transition_id).first()
        if not destination_state_obj:
            return False, "找不到工作流流转表"
        destination_state_id = destination_state_obj.destination_state_id

        # 取出下一个状态的状态 id
        # destination_state_id = -1
        # for transition_obj in transition_queryset:
        #     if transition_obj.id == transition_id:
        #         destination_state_id = transition_obj.destination_state_id
        #         break

        destination_state, msg = WorkflowStateService.get_workflow_state_by_id(
            destination_state_id)
        if not destination_state:
            return False, msg

        # 获取目标状态的信息，判断是由哪种类型哪种人员处理该工单。
        destination_participant_type_id = destination_state.participant_type_id
        destination_participant = destination_state.participant
        if destination_participant_type_id == CONSTANT_SERVICE.PARTICIPANT_TYPE_FIELD:
            # 获取工单字段的值, 因为是新建工单,记录还没实际生成，所以该字段只能在 request_data_dict 中
            field_value = request_data_dict.get(destination_participant, '')
            if not field_value:
                return False, "请求的数据中无此字段的值, 或值为空: {}".format(
                    destination_participant)
            destination_participant = field_value
            if len(field_value.split(',')) > 1:
                # 字段中包含多人
                destination_participant_type_id = CONSTANT_SERVICE.PARTICIPANT_TYPE_MULTI
            else:
                destination_participant_type_id = CONSTANT_SERVICE.PARTICIPANT_TYPE_PERSONAL
        # 字段在父工单中
        elif destination_participant_type_id == CONSTANT_SERVICE.PARTICIPANT_TYPE_PARENT_FIELD:
            destination_participant, msg = cls.get_ticket_field_value(
                parent_ticket_id, destination_participant)
            if len(destination_participant.split(',')) > 1:
                # 字段中包含多人
                destination_participant_type_id = CONSTANT_SERVICE.PARTICIPANT_TYPE_MULTI
            else:
                destination_participant_type_id = CONSTANT_SERVICE.PARTICIPANT_TYPE_PERSONAL
        elif destination_participant_type_id == CONSTANT_SERVICE.PARTICIPANT_TYPE_VARIABLE:
            if destination_participant == 'creator':
                destination_participant_type_id = CONSTANT_SERVICE.PARTICIPANT_TYPE_PERSONAL
                destination_participant = username
            elif destination_participant == 'creator_t1':
                # 获取用户的t1 或 审批人
                approver, msg = AccountBaseService.get_user_dept_approver(
                    username)
                if len(approver.split(',')) > 1:
                    # 字段中包含多人
                    destination_participant_type_id = CONSTANT_SERVICE.PARTICIPANT_TYPE_MULTI
                else:
                    destination_participant_type_id = CONSTANT_SERVICE.PARTICIPANT_TYPE_PERSONAL
                destination_participant = approver

        # 生成工单流水号
        ticket_sn, msg = cls.gen_ticket_sn(workflow_id)
        if not ticket_sn:
            return False, msg

        # 新建工单基础表数据
        new_ticket_obj = TicketRecord(
            sn=ticket_sn,
            title=request_data_dict.get('title', ''),
            workflow_id=workflow_id,
            state_id=destination_state_id,
            parent_ticket_id=parent_ticket_id,
            parent_ticket_state_id=parent_ticket_state_id,
            participant=destination_participant,
            participant_type_id=destination_participant_type_id,
            relation=username,
            creator=username,
            modifier=username,
            application_date=application_date)
        new_ticket_obj.save()
        # 新增关系人
        add_relation, msg = cls.get_ticket_dest_relation(
            destination_participant_type_id, destination_participant)
        if add_relation:
            new_relation, msg = cls.add_ticket_relation(
                new_ticket_obj.id, add_relation)
        # 新增自定义字段
        request_data_dict_allow = {}
        for key, value in request_data_dict.items():
            if key in update_field_list:
                request_data_dict_allow[key] = value
        update_ticket_custom_field_result, msg = cls.update_ticket_custom_field(
            new_ticket_obj.id, request_data_dict_allow)
        if update_ticket_custom_field_result is False:
            return False, msg

        async_diy_field_result, msg = cls.async_diy_field(username,
                                                          new_ticket_obj.id, request_data_dict)

        if async_diy_field_result is False:
            cls.ticket_delete('admin', str(new_ticket_obj.id))
            return False, msg

        # 新增流转记录
        new_ticket_flow_log_dict = dict(
            ticket_id=new_ticket_obj.id,
            transition_id=transition_id,
            suggestion=suggestion,
            participant_type_id=CONSTANT_SERVICE.PARTICIPANT_TYPE_PERSONAL,
            participant=username,
            state_id=start_state.id,
            creator=username)
        add_ticket_flow_log_result, msg = cls.add_ticket_flow_log(
            new_ticket_flow_log_dict)
        if not add_ticket_flow_log_result:
            return False, msg
        # 当下个状态为脚本处理时, 则开始执行脚本
        if destination_participant_type_id == CONSTANT_SERVICE.PARTICIPANT_TYPE_ROBOT:
            from backend.workflow.tasks import run_flow_task  # 放在文件开头会存在循环引用
            run_flow_task.apply_async(
                args=(
                    new_ticket_obj.id,
                    destination_participant,
                    destination_state_id,
                ),
                queue='yqpass')

        # 父工单逻辑处理
        if destination_state.type_id == CONSTANT_SERVICE.STATE_TYPE_END and new_ticket_obj.parent_ticket_id and \
                new_ticket_obj.parent_ticket_state_id:
            # 如果存在父工单，判断是否该父工单的下属子工单都已经结束状态，如果都是结束状态则自动流转父工单到下个状态
            other_sub_ticket_queryset = TicketRecord.objects.filter(
                parent_ticket_id=new_ticket_obj.parent_ticket_id,
                parent_ticket_state_id=new_ticket_obj.parent_ticket_state_id,
                is_deleted=0).all()
            other_sub_ticket_state_id_list = [
                other_sub_ticket.state_id
                for other_sub_ticket in other_sub_ticket_queryset
            ]
            if set(other_sub_ticket_state_id_list) == {
                new_ticket_obj.state_id
            }:
                parent_ticket_obj = TicketRecord.objects.filter(
                    id=new_ticket_obj.parent_ticket_id, is_deleted=0).first()
                parent_ticket_state_id = parent_ticket_obj.state_id
                parent_ticket_transition_queryset, msg = WorkflowTransitionService.get_state_transition_queryset(
                    parent_ticket_state_id)
                # 含有子工单的工单状态只支持单路径流转到下个状态
                parent_ticket_transition_id = parent_ticket_transition_queryset[
                    0].id
                cls.handle_ticket(
                    parent_ticket_obj.id,
                    dict(
                        transition_id=parent_ticket_transition_id,
                        username='admin',
                        suggestion='所有子工单处理完毕，自动流转'))
        return new_ticket_obj.id, ''

    @classmethod
    @auto_log
    def handle_ticket(cls, ticket_id, request_data_dict):
        """
        处理工单:校验必填参数,获取当前状态必填字段，更新工单基础字段，更新工单自定义字段， 更新工单流转记录，执行必要的脚本，通知消息
        :param ticket_id:
        :param request_data_dict:
        :return:
        """
        transition_id = request_data_dict.get('transition_id', '')
        username = request_data_dict.get('username', '')
        suggestion = request_data_dict.get('suggestion', '')

        if not (transition_id and username):
            return False, "参数不合法, 请提供username, transition_id"
        # transition_id = int(transition_id)
        ticket_obj = TicketRecord.objects.filter(
            id=ticket_id, is_deleted=0).first()
        if not ticket_obj:
            return False, "工单不存在或已被删除"
        source_ticket_state_id = ticket_obj.state_id

        # 判断用户是否有权限处理该工单
        has_permission, msg = ticket_handle_permission_check(
            ticket_id, username)
        if not has_permission:
            return False, msg
        if msg['need_accept']:
            return False, "需要先接单再处理"
        if msg['in_add_node']:
            return False, "工单当前处于加签中, 只允许加签完成操作"

        # 校验当前工单必填字段
        state_obj, msg = WorkflowStateService.get_workflow_state_by_id(
            source_ticket_state_id)
        if not state_obj:
            return False, msg
        state_field_str = state_obj.state_field_str
        state_field_dict = json.loads(state_field_str)
        require_field_list, update_field_list = [], []
        update_field_dict = {}
        for key, value in state_field_dict.items():
            if value == CONSTANT_SERVICE.FIELD_ATTRIBUTE_REQUIRED:
                require_field_list.append(key)
            update_field_list.append(key)
            if request_data_dict.get(key):
                update_field_dict[key] = request_data_dict.get(key)

        # 校验是否所有必填字段都有提供, 如果 transition_id 对应设置为不校验必填则直接通过
        req_transition_obj, msg = WorkflowTransitionService.get_workflow_transition_by_id(
            transition_id)
        if req_transition_obj.field_require_check:
            request_field_arg_list = [
                key for key, value in request_data_dict.items()
                if (key not in ['workflow_id', 'suggestion', 'username'])
            ]
            for require_field in require_field_list:
                if require_field not in request_field_arg_list:
                    return False, "handle_ticket: 此工单的必填字段为: {}".format(
                        ','.join(require_field_list))

        # 获取 transition_id 对应的下个状态的信息
        transition_queryset, msg = WorkflowTransitionService.get_state_transition_queryset(
            source_ticket_state_id)
        if transition_queryset is False:
            return False, msg
        allow_transition_id_list = [
            transition.id for transition in transition_queryset
        ]
        if transition_id not in allow_transition_id_list:
            return False, "transition_id 不合法"
        destination_state_id = -1
        for transition_obj in transition_queryset:
            if transition_obj.id == transition_id:
                destination_state_id = transition_obj.destination_state_id
                break
        destination_state, msg = WorkflowStateService.get_workflow_state_by_id(
            destination_state_id)
        if not destination_state:
            return False, msg

        # 获取目标状态信息
        destination_participant_type_id = destination_state.participant_type_id
        destination_participant = destination_state.participant
        if destination_participant_type_id == CONSTANT_SERVICE.PARTICIPANT_TYPE_DEPT:
            username_list, msg = AccountBaseService.get_dept_username_list(
                destination_participant)
            add_relation = ','.join(username_list)
        elif destination_participant_type_id == CONSTANT_SERVICE.PARTICIPANT_TYPE_ROLE:
            username_list, msg = AccountBaseService.get_role_username_list(
                destination_participant)
            add_relation = ','.join(username_list)
        elif destination_participant_type_id == CONSTANT_SERVICE.PARTICIPANT_TYPE_FIELD:
            destination_participant, msg = cls.get_ticket_field_value(
                ticket_id, destination_participant)
            if not destination_participant:
                return False, msg
            destination_participant_type_id = CONSTANT_SERVICE.PARTICIPANT_TYPE_PERSONAL
            add_relation = destination_participant
            if len(destination_participant.split(',')) > 1:
                # 多人的情况
                destination_participant_type_id = CONSTANT_SERVICE.PARTICIPANT_TYPE_MULTI
        elif destination_participant_type_id == CONSTANT_SERVICE.PARTICIPANT_TYPE_PARENT_FIELD:
            destination_participant, msg = cls.get_ticket_field_value(
                ticket_obj.parent_ticket_id, destination_participant)
            destination_participant_type_id = CONSTANT_SERVICE.PARTICIPANT_TYPE_PERSONAL
            if len(destination_participant.split(',')) > 1:
                destination_participant_type_id = CONSTANT_SERVICE.PARTICIPANT_TYPE_FIELD
            add_relation = destination_participant
        elif destination_participant_type_id == CONSTANT_SERVICE.PARTICIPANT_TYPE_VARIABLE:
            if destination_participant == 'creator':
                destination_participant_type_id = CONSTANT_SERVICE.PARTICIPANT_TYPE_PERSONAL
                destination_participant = ticket_obj.creator
            elif destination_participant == 'creator_t1':
                # 获取用户的 t1 或审批人
                approver, msg = AccountBaseService.get_user_dept_approver(
                    ticket_obj.creator)
                destination_participant_type_id = CONSTANT_SERVICE.PARTICIPANT_TYPE_PERSONAL
                if len(approver.split(',')) > 1:
                    destination_participant_type_id = CONSTANT_SERVICE.PARTICIPANT_TYPE_MULTI
                destination_participant = approver
            add_relation = destination_participant
        elif destination_participant_type_id == CONSTANT_SERVICE.PARTICIPANT_TYPE_ROBOT:
            add_relation = ''
        else:
            add_relation = destination_participant

        # 更新工单信息: 包含基础字段和自定义字段,

        new_ralation, msg = cls.add_ticket_relation(ticket_id, add_relation)
        # 记得刷新记录
        ticket_obj = TicketRecord.objects.filter(
            id=ticket_id, is_deleted=False).first()
        ticket_obj.state_id = destination_state_id
        ticket_obj.participant_type_id = destination_participant_type_id
        ticket_obj.participant = destination_participant
        ticket_obj.save()

        # 只更新需要更新的字段
        request_update_dict = {}
        for key, value in request_data_dict.items():
            if key in update_field_list:
                request_update_dict[key] = value
        update_ticket_custom_field_result, msg = cls.update_ticket_field_value(
            ticket_id, update_field_dict)
        if update_ticket_custom_field_result is False:
            return False, msg
        async_diy_field_result, msg = cls.async_diy_field(username,
                                                          ticket_id, request_data_dict)
        if async_diy_field_result is False:
            cls.ticket_delete('admin', str(ticket_id))
            return False, msg

        # 更新工单流转记录, 执行脚本, 通知信息等
        cls.add_ticket_flow_log(
            dict(
                ticket_id=ticket_id,
                transition_id=transition_id,
                suggestion=suggestion,
                participant_type_id=CONSTANT_SERVICE.PARTICIPANT_TYPE_PERSONAL,
                participant=username,
                state_id=source_ticket_state_id,
                creator=username))

        if destination_state.type_id == CONSTANT_SERVICE.STATE_TYPE_END and ticket_obj.parent_ticket_id and ticket_obj.parent_ticket_state_id:
            # 如果存在父工单, 判断是否该父工单下的子工单都已经结束, 如果结束则父工单自动流转到下个状态
            other_sub_ticket_queryset = TicketRecord.objects.filter(
                parent_ticket_id=ticket_obj.parent_ticket_id,
                parent_ticket_state_id=ticket_obj.parent_ticket_state_id,
                is_deleted=0).all()
            other_sub_ticket_state_id_list = [
                other_sub_ticket.state_id
                for other_sub_ticket in other_sub_ticket_queryset
            ]
            if set(other_sub_ticket_state_id_list) == {ticket_obj.state_id}:
                parent_ticket_obj = TicketRecord.objects.filter(
                    id=ticket_obj.parent_ticket_id, is_deleted=0).first()
                parent_ticket_state_id = parent_ticket_obj.state_id
                parent_ticket_transition_queryset, msg = WorkflowTransitionService.get_state_transition_queryset(
                    parent_ticket_state_id)
                parent_ticket_transition_id = parent_ticket_transition_queryset[
                    0].id
                cls.handle_ticket(
                    parent_ticket_obj.id,
                    dict(
                        transition_id=parent_ticket_transition_id,
                        username='admin',
                        suggetion="所有子工单已处理完毕, 自动流转"))
        # 如果下个流转状态是脚本
        if destination_participant_type_id == CONSTANT_SERVICE.PARTICIPANT_TYPE_ROBOT:
            from backend.workflow.tasks import run_flow_task  # 放在文件开头会存在循环引用
            run_flow_task_result = run_flow_task.apply_async(
                args=(
                    ticket_id,
                    destination_participant,
                    destination_state_id,
                ),
                queue='yqpass')

        # 通知信息
        return True, ''

    @classmethod
    @auto_log
    def get_ticket_detail(cls, ticket_id, username):
        """
        获取工单详情,
        :param ticket_id:
        :param username:
        :return:
        """
        handle_permission, msg = ticket_handle_permission_check(
            ticket_id, username)
        if not handle_permission:
            view_permission, msg = ticket_view_permission_check(
                ticket_id, username)
            if not view_permission:
                return False, msg

        ticket_obj = TicketRecord.objects.filter(
            id=ticket_id, is_deleted=0).first()
        field_list, msg = cls.get_ticket_base_field_list(ticket_id)
        if field_list is False:
            return False, msg

        new_field_list = []
        if handle_permission:
            state_obj, msg = WorkflowStateService.get_workflow_state_by_id(
                ticket_obj.state_id)
            if not state_obj:
                return False, msg
            state_field_str = state_obj.state_field_str
            state_field_dict = json.loads(state_field_str)
            state_field_key_list = state_field_dict.keys()
            for field in field_list:
                if field['field_key'] in state_field_key_list:
                    field['field_attribute'] = state_field_dict[
                        field['field_key']]
                    new_field_list.append(field)
                elif field['field_key'] in [
                    'participant_name', 'state_name', 'workflow_name'
                ]:
                    new_field_list.append(field)
        else:
            workflow_obj, msg = WorkflowBaseService.get_by_id(
                workflow_id=ticket_obj.workflow_id)
            display_form_field_list = json.loads(workflow_obj.display_form_str)
            for field in field_list:
                if field['field_key'] in display_form_field_list:
                    new_field_list.append(field)
                elif field['field_key'] in [
                    'participant_name', 'state_name', 'workflow_name'
                ]:
                    new_field_list.append(field)

        new_field_list = sorted(new_field_list, key=lambda r: r['order_id'])
        allow_transition_dict, msg = cls.get_ticket_transition(
            ticket_id, username)
        if allow_transition_dict is False:
            allow_transition_dict = ''

        return dict(id=ticket_obj.id, sn=ticket_obj.sn, title=ticket_obj.title, state_id=ticket_obj.state_id,
                    parent_ticket_id=ticket_obj.parent_ticket_id, participant=ticket_obj.participant,
                    participant_type_id=ticket_obj.participant_type_id, workflow_id=ticket_obj.workflow_id,
                    creator=ticket_obj.creator,
                    modifier=ticket_obj.modifier,
                    relation=ticket_obj.relation,
                    application_date=str(ticket_obj.application_date)[0:10],
                    gmt_created=str(ticket_obj.gmt_created)[0:19],
                    gmt_modified=str(ticket_obj.gmt_modified)[0:19],
                    transition=allow_transition_dict,
                    field_list=new_field_list), ''

    @classmethod
    @auto_log
    def get_ticket_format_participant_info(cls, ticket_id):
        """
        获取工单处理人信息
        :param cls:
        :param ticket_id:
        :return:
        """
        ticket_obj = TicketRecord.objects.filter(
            id=ticket_id, is_deleted=0).first()
        participant = ticket_obj.participant
        participant_name = ticket_obj.participant
        participant_type_id = ticket_obj.participant_type_id
        participant_type_name = ''
        participant_alias = ''
        if participant_type_id == CONSTANT_SERVICE.PARTICIPANT_TYPE_PERSONAL:
            participant_type_name = "个人"
            participant_user_obj, msg = AccountBaseService.get_user_by_username(
                participant)
            if not participant_user_obj:
                return False, "对应处理用户不存在"
            participant_alias = participant_user_obj.alias
        elif participant_type_id == CONSTANT_SERVICE.PARTICIPANT_TYPE_MULTI:
            participant_type_name = "多人"
            participant_name_list = participant_name.split(',')
            participant_alias_list = []
            for name in participant_name_list:
                participant_user_obj, msg = AccountBaseService.get_user_by_username(
                    name)
                if participant_user_obj is False:
                    continue
                participant_alias_list.append(participant_user_obj.alias)
            participant_alias = ','.join(participant_alias_list)
        elif participant_type_id == CONSTANT_SERVICE.PARTICIPANT_TYPE_ROLE:
            participant_type_name = "角色"
            role_obj, msg = AccountBaseService.get_role_by_id(int(participant))
            participant_name = role_obj.name
            participant_alias = participant_name
        elif participant_type_id == CONSTANT_SERVICE.PARTICIPANT_TYPE_DEPT:
            participant_type_name = "部门"
            dept_obj, msg = AccountBaseService.get_dept_by_id(int(participant))
            participant_name = dept_obj.name
            participant_alias = participant_name
        return dict(
            participant=participant,
            participant_name=participant_name,
            participant_type_id=participant_type_id,
            participant_type_name=participant_type_name,
            participant_alias=participant_alias), ''

    @classmethod
    @auto_log
    def get_ticket_field_value(cls, ticket_id, field_key):
        """
        获取工单字段的值
        :param ticket_id:
        :param field_key:
        :return:
        """
        # 分为基础字段和自定义字段两种
        if field_key in CONSTANT_SERVICE.TICKET_BASE_FIELD_LIST:
            ticket_obj = TicketRecord.objects.filter(
                id=ticket_id, is_deleted=0).first()
            if not ticket_obj:
                return False, "ticket_id对应工单不存在"
            ticket_obj_dict = ticket_obj.__dict__
            value, msg = ticket_obj_dict.get(field_key), ''
        else:
            value, msg = cls.get_ticket_custom_field_value(
                ticket_id, field_key)
        return value, msg

    @classmethod
    @auto_log
    def get_ticket_custom_field_value(cls, ticket_id, field_key):
        """
        获取工单的自定义字段的值
        :param ticket:
        :param field_key:
        :return:
        """
        format_field_key_dict, msg = cls.get_ticket_custom_field_key_dict(
            ticket_id)
        if not format_field_key_dict:
            return False, msg

        field_type_id = format_field_key_dict[field_key]['field_type_id']
        ticket_custom_field_obj = TicketCustomField.objects.filter(
            field_key=field_key, ticket_id=ticket_id, is_deleted=0).first()

        value = None
        if not ticket_custom_field_obj:
            # 可能还为空
            value = None
        else:
            if field_type_id == CONSTANT_SERVICE.FIELD_TYPE_STR:
                value = ticket_custom_field_obj.char_value
            elif field_type_id == CONSTANT_SERVICE.FIELD_TYPE_INT:
                value = ticket_custom_field_obj.int_value
            elif field_type_id == CONSTANT_SERVICE.FIELD_TYPE_FLOAT:
                value = ticket_custom_field_obj.float_value
            elif field_type_id == CONSTANT_SERVICE.FIELD_TYPE_BOOL:
                value = ticket_custom_field_obj.bool_value
            elif field_type_id == CONSTANT_SERVICE.FIELD_TYPE_DATE:
                value = str(ticket_custom_field_obj.date_value)
            elif field_type_id == CONSTANT_SERVICE.FIELD_TYPE_DATETIME:
                value = str(ticket_custom_field_obj.datetime_value)
            elif field_type_id == CONSTANT_SERVICE.FIELD_TYPE_RADIO:
                value = ticket_custom_field_obj.radio_value
            elif field_type_id == CONSTANT_SERVICE.FIELD_TYPE_CHECKBOX:
                value = ticket_custom_field_obj.checkbox_value
            elif field_type_id == CONSTANT_SERVICE.FIELD_TYPE_SELECT:
                value = ticket_custom_field_obj.select_value
            elif field_type_id == CONSTANT_SERVICE.FIELD_TYPE_MULTI_SELECT:
                value = ticket_custom_field_obj.multi_select_value
            elif field_type_id == CONSTANT_SERVICE.FIELD_TYPE_TEXT:
                value = ticket_custom_field_obj.text_value
            elif field_type_id == CONSTANT_SERVICE.FIELD_TYPE_USERNAME:
                value = ticket_custom_field_obj.username_value
            elif field_type_id == CONSTANT_SERVICE.FIELD_TYPE_MULTI_USERNAME:
                value = ticket_custom_field_obj.multi_username_value

        return value, ''

    @classmethod
    @auto_log
    def get_ticket_custom_field_key_dict(cls, ticket_id):
        """
        获取工单的自定义字段的 dict
        :param ticket_id:
        :return:
        """
        ticket_obj = TicketRecord.objects.filter(
            id=ticket_id, is_deleted=0).first()
        custom_field_queryset = CustomField.objects.filter(
            is_deleted=0, workflow_id=ticket_obj.workflow_id).all()
        format_field_key_dict = {}
        for custom_field in custom_field_queryset:
            format_field_key_dict[custom_field.field_key] = dict(
                field_type_id=custom_field.field_type_id,
                field_name=custom_field.field_name,
                boolean_field_display=custom_field.boolean_field_display,
                field_choice=custom_field.field_choice,
                field_from='custom')
        return format_field_key_dict, ''

    @classmethod
    def gen_ticket_sn(cls, workflow_id):
        # 统计当前天数的工单数量 +1
        today = str(datetime.datetime.now())[:10] + ' 00:00:00'
        tomorrow = str(datetime.datetime.now() +
                       datetime.timedelta(days=1))[:10] + ' 00:00:00'
        ticket_day_count = TicketRecord.objects.filter(
            workflow_id=workflow_id,
            gmt_created__gte=today,
            gmt_created__lte=tomorrow).count()
        index_count = ticket_day_count + 1
        now_day = datetime.datetime.now()

        return '{0:0>4}{1:0>2}{2:0>2}-{3:0>2}'.format(
            now_day.year, now_day.month, now_day.day, index_count), ''

    @classmethod
    def update_ticket_custom_field(cls, ticket_id, update_dict):
        """
        更新工单自定义值
        :param ticket_id:
        :param update_dict:
        :return:
        """
        # 获取工单的自定义字段
        ticket_obj = TicketRecord.objects.filter(
            id=ticket_id, is_deleted=0).first()
        format_custom_field_dict, msg = WorkflowCustomFieldService.get_workflow_custom_field(
            ticket_obj.workflow_id)
        if format_custom_field_dict is False:
            return False, msg
        custom_field_key_list = [
            key for key, value in format_custom_field_dict.items()
        ]
        updated_key_list = []

        # 直接遍历处理
        for key, value in update_dict.items():
            if key in custom_field_key_list:
                # 存在则更新
                updated_key_list.append(key)
                ticket_custom_field_queryset = TicketCustomField.objects.filter(
                    ticket_id=ticket_id, field_key=key)
                field_type_id = format_custom_field_dict[key]['field_type_id']
                if ticket_custom_field_queryset:
                    if field_type_id == CONSTANT_SERVICE.FIELD_TYPE_STR:
                        ticket_custom_field_queryset.update(
                            char_value=update_dict.get(key))
                    elif field_type_id == CONSTANT_SERVICE.FIELD_TYPE_INT:
                        ticket_custom_field_queryset.update(
                            int_value=int(update_dict.get(key)))
                    elif field_type_id == CONSTANT_SERVICE.FIELD_TYPE_FLOAT:
                        ticket_custom_field_queryset.update(
                            float_value=update_dict.get(key))
                    elif field_type_id == CONSTANT_SERVICE.FIELD_TYPE_BOOL:
                        ticket_custom_field_queryset.update(
                            bool_value=int(update_dict.get(key)))
                    elif field_type_id == CONSTANT_SERVICE.FIELD_TYPE_DATE:
                        ticket_custom_field_queryset.update(
                            date_value=update_dict.get(key))
                    elif field_type_id == CONSTANT_SERVICE.FIELD_TYPE_DATETIME:
                        ticket_custom_field_queryset.update(
                            datetime_value=update_dict.get(key))
                    elif field_type_id == CONSTANT_SERVICE.FIELD_TYPE_RADIO:
                        ticket_custom_field_queryset.update(
                            radio_value=update_dict.get(key))
                    elif field_type_id == CONSTANT_SERVICE.FIELD_TYPE_CHECKBOX:
                        ticket_custom_field_queryset.update(
                            checkbox_value=update_dict.get(key))
                    elif field_type_id == CONSTANT_SERVICE.FIELD_TYPE_SELECT:
                        ticket_custom_field_queryset.update(
                            select_value=update_dict.get(key))
                    elif field_type_id == CONSTANT_SERVICE.FIELD_TYPE_MULTI_SELECT:
                        ticket_custom_field_queryset.update(
                            multi_select_value=update_dict.get(key))
                    elif field_type_id == CONSTANT_SERVICE.FIELD_TYPE_TEXT:
                        ticket_custom_field_queryset.update(
                            text_value=update_dict.get(key))
                    elif field_type_id == CONSTANT_SERVICE.FIELD_TYPE_USERNAME:
                        ticket_custom_field_queryset.update(
                            username_value=update_dict.get(key))
                    elif field_type_id == CONSTANT_SERVICE.FIELD_TYPE_MULTI_USERNAME:
                        ticket_custom_field_queryset.update(
                            multi_username_value=update_dict.get(key))
                else:
                    new_ticket_custom_field_record = TicketCustomField.objects.none(
                    )
                    if field_type_id == CONSTANT_SERVICE.FIELD_TYPE_STR:
                        new_ticket_custom_field_record = TicketCustomField(
                            name=format_custom_field_dict[key]['field_name'],
                            ticket_id=ticket_id,
                            field_key=key,
                            field_type_id=field_type_id,
                            char_value=update_dict.get(key))
                    elif field_type_id == CONSTANT_SERVICE.FIELD_TYPE_INT:
                        new_ticket_custom_field_record = TicketCustomField(
                            name=format_custom_field_dict[key]['field_name'],
                            ticket_id=ticket_id,
                            field_key=key,
                            field_type_id=field_type_id,
                            int_value=update_dict.get(key))
                    elif field_type_id == CONSTANT_SERVICE.FIELD_TYPE_FLOAT:
                        new_ticket_custom_field_record = TicketCustomField(
                            name=format_custom_field_dict[key]['field_name'],
                            ticket_id=ticket_id,
                            field_key=key,
                            field_type_id=field_type_id,
                            float_value=update_dict.get(key))
                    elif field_type_id == CONSTANT_SERVICE.FIELD_TYPE_BOOL:
                        new_ticket_custom_field_record = TicketCustomField(
                            name=format_custom_field_dict[key]['field_name'],
                            ticket_id=ticket_id,
                            field_key=key,
                            field_type_id=field_type_id,
                            bool_value=update_dict.get(key))
                    elif field_type_id == CONSTANT_SERVICE.FIELD_TYPE_DATE:
                        new_ticket_custom_field_record = TicketCustomField(
                            name=format_custom_field_dict[key]['field_name'],
                            ticket_id=ticket_id,
                            field_key=key,
                            field_type_id=field_type_id,
                            date_value=update_dict.get(key))
                    elif field_type_id == CONSTANT_SERVICE.FIELD_TYPE_DATETIME:
                        new_ticket_custom_field_record = TicketCustomField(
                            name=format_custom_field_dict[key]['field_name'],
                            ticket_id=ticket_id,
                            field_key=key,
                            field_type_id=field_type_id,
                            datetime_value=update_dict.get(key))
                    elif field_type_id == CONSTANT_SERVICE.FIELD_TYPE_RADIO:
                        new_ticket_custom_field_record = TicketCustomField(
                            name=format_custom_field_dict[key]['field_name'],
                            ticket_id=ticket_id,
                            field_key=key,
                            field_type_id=field_type_id,
                            radio_value=update_dict.get(key))
                    elif field_type_id == CONSTANT_SERVICE.FIELD_TYPE_CHECKBOX:
                        new_ticket_custom_field_record = TicketCustomField(
                            name=format_custom_field_dict[key]['field_name'],
                            ticket_id=ticket_id,
                            field_key=key,
                            field_type_id=field_type_id,
                            checkbox_value=update_dict.get(key))
                    elif field_type_id == CONSTANT_SERVICE.FIELD_TYPE_SELECT:
                        new_ticket_custom_field_record = TicketCustomField(
                            name=format_custom_field_dict[key]['field_name'],
                            ticket_id=ticket_id,
                            field_key=key,
                            field_type_id=field_type_id,
                            select_value=update_dict.get(key))
                    elif field_type_id == CONSTANT_SERVICE.FIELD_TYPE_MULTI_SELECT:
                        new_ticket_custom_field_record = TicketCustomField(
                            name=format_custom_field_dict[key]['field_name'],
                            ticket_id=ticket_id,
                            field_key=key,
                            field_type_id=field_type_id,
                            multi_select_value=update_dict.get(key))
                    elif field_type_id == CONSTANT_SERVICE.FIELD_TYPE_TEXT:
                        new_ticket_custom_field_record = TicketCustomField(
                            name=format_custom_field_dict[key]['field_name'],
                            ticket_id=ticket_id,
                            field_key=key,
                            field_type_id=field_type_id,
                            text_value=update_dict.get(key))
                    elif field_type_id == CONSTANT_SERVICE.FIELD_TYPE_USERNAME:
                        new_ticket_custom_field_record = TicketCustomField(
                            name=format_custom_field_dict[key]['field_name'],
                            ticket_id=ticket_id,
                            field_key=key,
                            field_type_id=field_type_id,
                            username_value=update_dict.get(key))
                    elif field_type_id == CONSTANT_SERVICE.FIELD_TYPE_MULTI_USERNAME:
                        new_ticket_custom_field_record = TicketCustomField(
                            name=format_custom_field_dict[key]['field_name'],
                            ticket_id=ticket_id,
                            field_key=key,
                            field_type_id=field_type_id,
                            multi_username_value=update_dict.get(key))
                    new_ticket_custom_field_record.save()

        return updated_key_list, ''

    @classmethod
    @auto_log
    def add_ticket_flow_log(cls, ticket_flow_log_dict):
        """
        新增工单流转记录
        :param ticket_flow_log_dict:
        :return:
        """
        new_ticket_flow_log = TicketFlowLog(**ticket_flow_log_dict)
        new_ticket_flow_log.save()
        return new_ticket_flow_log.id, ''

    @classmethod
    @auto_log
    def add_ticket_relation(cls, ticket_id, user_str):
        """
        新增工单的关联人
        :param ticket_id:
        :param user_str:
        :return:
        """
        ticket_obj = TicketRecord.objects.filter(
            id=ticket_id, is_deleted=0).first()
        if not ticket_obj:
            return False, "工单不存在或已被删除"

        # 去重 and 去空元素
        new_relation_set = set(
            ticket_obj.relation.split(',') + user_str.split(','))
        new_relation_list = [
            relation for relation in new_relation_set if relation
        ]
        new_relation = ','.join(new_relation_list)
        ticket_obj.relation = new_relation
        ticket_obj.save()
        return new_relation, ''

    @classmethod
    @auto_log
    def update_ticket_field_value(cls, ticket_id, update_dict):
        """
        更新工单字段的值
        :param ticket_id:
        :param update_dict:
        :return:
        """
        base_field_dict = {}
        for key, value in update_dict.items():
            if key in CONSTANT_SERVICE.TICKET_BASE_FIELD_LIST:
                base_field_dict[key] = value
        if base_field_dict:
            TicketRecord.objects.filter(
                id=ticket_id, is_deleted=0).update(**base_field_dict)
        updated_key_list = cls.update_ticket_custom_field(
            ticket_id, update_dict)

        return updated_key_list, ''

    @classmethod
    @auto_log
    def get_ticket_base_field_list(cls, ticket_id):
        """
        获取工单字段信息
        :param ticket_id:
        :return:
        """
        ticket_obj = TicketRecord.objects.filter(
            id=ticket_id, is_deleted=0).first()
        state_obj, msg = WorkflowStateService.get_workflow_state_by_id(
            ticket_obj.state_id)
        if not state_obj:
            return False, msg
        state_name = state_obj.name

        # 工单基础字段及属性
        field_list = []
        participant_info_dict, msg = cls.get_ticket_format_participant_info(
            ticket_id)
        if participant_info_dict is False:
            return False, msg

        workflow_obj, msg = WorkflowBaseService.get_by_id(
            ticket_obj.workflow_id)
        workflow_name = workflow_obj.name

        field_list.append(
            dict(
                field_key='sn',
                name="工单编号",
                field_value=ticket_obj.sn,
                order_id=0,
                field_type_id=CONSTANT_SERVICE.FIELD_TYPE_STR,
                field_attribute=CONSTANT_SERVICE.FIELD_ATTRIBUTE_RO))
        field_list.append(
            dict(
                field_key='title',
                name="标题",
                field_value=ticket_obj.title,
                order_id=20,
                field_type_id=CONSTANT_SERVICE.FIELD_TYPE_STR,
                field_attribute=CONSTANT_SERVICE.FIELD_ATTRIBUTE_RO))
        field_list.append(
            dict(
                field_key='state_id',
                name="状态",
                field_value=ticket_obj.state_id,
                order_id=40,
                field_type_id=CONSTANT_SERVICE.FIELD_TYPE_STR,
                field_attribute=CONSTANT_SERVICE.FIELD_ATTRIBUTE_RO))
        field_list.append(
            dict(
                field_key='participant_name',
                name="当前处理人",
                field_value=participant_info_dict['participant_name'],
                order_id=50,
                field_type_id=CONSTANT_SERVICE.FIELD_TYPE_STR,
                field_attribute=CONSTANT_SERVICE.FIELD_ATTRIBUTE_RO))
        field_list.append(
            dict(
                field_key='participant_alias',
                name="当前处理人",
                field_value=participant_info_dict['participant_alias'],
                order_id=55,
                field_type_id=CONSTANT_SERVICE.FIELD_TYPE_STR,
                field_attribute=CONSTANT_SERVICE.FIELD_ATTRIBUTE_RO))
        field_list.append(
            dict(
                field_key='workflow_name',
                name="工作流名称",
                field_value=workflow_name,
                order_id=60,
                field_type_id=CONSTANT_SERVICE.FIELD_TYPE_STR,
                field_attribute=CONSTANT_SERVICE.FIELD_ATTRIBUTE_RO))
        field_list.append(
            dict(
                field_key='creator',
                name="创建人",
                field_value=ticket_obj.creator,
                order_id=80,
                field_type_id=CONSTANT_SERVICE.FIELD_TYPE_STR,
                field_attribute=CONSTANT_SERVICE.FIELD_ATTRIBUTE_RO))
        field_list.append(
            dict(
                field_key='modifier',
                name="最后修改人",
                field_value=ticket_obj.modifier,
                order_id=85,
                field_type_id=CONSTANT_SERVICE.FIELD_TYPE_STR,
                field_attribute=CONSTANT_SERVICE.FIELD_ATTRIBUTE_RO))
        field_list.append(
            dict(
                field_key='application_date',
                name="建单日期",
                field_value=str(ticket_obj.application_date)[:10],
                order_id=90,
                field_type_id=CONSTANT_SERVICE.FIELD_TYPE_STR,
                field_attribute=CONSTANT_SERVICE.FIELD_ATTRIBUTE_RO))
        field_list.append(
            dict(
                field_key='gmt_created',
                name="创建时间",
                field_value=str(ticket_obj.gmt_created)[:19],
                order_id=100,
                field_type_id=CONSTANT_SERVICE.FIELD_TYPE_STR,
                field_attribute=CONSTANT_SERVICE.FIELD_ATTRIBUTE_RO))
        field_list.append(
            dict(
                field_key='gmt_modified',
                name="更新时间",
                field_value=str(ticket_obj.gmt_modified)[:19],
                order_id=120,
                field_type_id=CONSTANT_SERVICE.FIELD_TYPE_STR,
                field_attribute=CONSTANT_SERVICE.FIELD_ATTRIBUTE_RO))
        field_list.append(
            dict(
                field_key='state_name',
                name="状态名",
                field_value=state_name,
                order_id=41,
                field_type_id=CONSTANT_SERVICE.FIELD_TYPE_STR,
                field_attribute=CONSTANT_SERVICE.FIELD_ATTRIBUTE_RO))

        # 工单所有自定义字段
        custom_field_dict, msg = WorkflowCustomFieldService.get_workflow_custom_field(
            ticket_obj.workflow_id)
        for key, value in custom_field_dict.items():
            field_type_id = value['field_type_id']
            ticket_custom_field_obj = TicketCustomField.objects.filter(
                ticket_id=ticket_id, field_key=key, is_deleted=0).first()
            # 尚未赋值
            if not ticket_custom_field_obj:
                field_value = None
            else:
                field_value = ''
                # 根据字段类型 获取对应列的值

                if field_type_id == CONSTANT_SERVICE.FIELD_TYPE_STR:
                    field_value = ticket_custom_field_obj.char_value
                elif field_type_id == CONSTANT_SERVICE.FIELD_TYPE_INT:
                    field_value = ticket_custom_field_obj.int_value
                elif field_type_id == CONSTANT_SERVICE.FIELD_TYPE_FLOAT:
                    field_value = ticket_custom_field_obj.float_value
                elif field_type_id == CONSTANT_SERVICE.FIELD_TYPE_BOOL:
                    field_value = ticket_custom_field_obj.bool_value
                elif field_type_id == CONSTANT_SERVICE.FIELD_TYPE_DATE:
                    field_value = str(ticket_custom_field_obj.date_value)
                elif field_type_id == CONSTANT_SERVICE.FIELD_TYPE_DATETIME:
                    field_value = str(ticket_custom_field_obj.datetime_value)
                elif field_type_id == CONSTANT_SERVICE.FIELD_TYPE_RADIO:
                    field_value = ticket_custom_field_obj.radio_value
                elif field_type_id == CONSTANT_SERVICE.FIELD_TYPE_CHECKBOX:
                    field_value = ticket_custom_field_obj.checkbox_value
                elif field_type_id == CONSTANT_SERVICE.FIELD_TYPE_SELECT:
                    field_value = ticket_custom_field_obj.select_value
                elif field_type_id == CONSTANT_SERVICE.FIELD_TYPE_MULTI_SELECT:
                    field_value = ticket_custom_field_obj.multi_select_value
                elif field_type_id == CONSTANT_SERVICE.FIELD_TYPE_TEXT:
                    field_value = ticket_custom_field_obj.text_value
                elif field_type_id == CONSTANT_SERVICE.FIELD_TYPE_USERNAME:
                    field_value = ticket_custom_field_obj.username_value
                elif field_type_id == CONSTANT_SERVICE.FIELD_TYPE_MULTI_USERNAME:
                    field_value = ticket_custom_field_obj.multi_username_value

            field_list.append(
                dict(
                    field_key=key,
                    field_name=custom_field_dict[key]['field_name'],
                    field_value=field_value,
                    order_id=custom_field_dict[key]['order_id'],
                    field_type_id=field_type_id,
                    field_attribute=CONSTANT_SERVICE.FIELD_ATTRIBUTE_RO,
                    field_choice=json.loads(
                        custom_field_dict[key]['field_choice']),
                ))
        return field_list, ''

    @classmethod
    @auto_log
    def get_ticket_transition(cls, ticket_id, username):
        """
        针对工单当前状态, 获取可以进行的操作
        :param ticket_id:
        :param username:
        :return:
        """
        handle_permission, msg = ticket_handle_permission_check(
            ticket_id, username)
        if not handle_permission:
            return False, msg

        ticket_obj = TicketRecord.objects.filter(
            id=ticket_id, is_deleted=0).first()
        if not ticket_obj:
            return False, "工单不存在或已被删除"

        if ticket_obj.in_add_node:
            # 加签状态中, 只允许"完成"操作,  完成后工单处理人设为 add_node_man
            transition_dict_list = [
                dict(
                    transition_id=0,
                    transition_name='完成',
                    field_require_check=False,
                    is_accept=False,
                    in_add_node=True)
            ]
            return transition_dict_list, ''
        if msg['need_accept']:
            transition_dict_list = [
                dict(
                    transition_id=0,
                    transition_name='接单',
                    field_require_check=False,
                    is_accept=True,
                    in_add_node=False)
            ]
            return transition_dict_list, ''

        transition_queryset, msg = WorkflowTransitionService.get_state_transition_queryset(
            ticket_obj.state_id)
        if transition_queryset is False:
            return False, msg
        transition_dict_list = []
        for transition in transition_queryset:
            transition_dict = dict(
                transition_id=transition.id,
                transition_name=transition.name,
                field_require_check=transition.field_require_check,
                is_accept=False,
                in_add_node=False)
            transition_dict_list.append(transition_dict)
        return transition_dict_list, ''

    @classmethod
    @auto_log
    def get_ticket_flow_log(cls, ticket_id, per_page, page):
        """
        获取工单流转记录
        :param ticket_id:
        :param per_page:
        :param page:
        :return:
        """
        ticket_flow_log_queryset = TicketFlowLog.objects.filter(
            ticket_id=ticket_id, is_deleted=0).all().order_by('-id')
        paginator = Paginator(ticket_flow_log_queryset, per_page)

        try:
            ticket_result_paginator = paginator.page(page)
        except PageNotAnInteger:
            ticket_result_paginator = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results
            ticket_result_paginator = paginator.page(paginator.num_pages)

        ticket_flow_log_restful_list = []
        for ticket_flow_log in ticket_result_paginator.object_list:
            state_obj, msg = WorkflowStateService.get_workflow_state_by_id(
                ticket_flow_log.state_id)
            if ticket_flow_log.transition_id:
                transition_obj, msg = WorkflowTransitionService.get_workflow_transition_by_id(
                    ticket_flow_log.transition_id)
                transition_name = transition_obj.name
            else:
                # 考虑到人工干预修改工单状态， transition_id为0
                if ticket_flow_log.intervene_type_id == CONSTANT_SERVICE.TRANSITION_INTERVENE_TYPE_DELIVER:
                    transition_name = '转交操作'
                elif ticket_flow_log.intervene_type_id == CONSTANT_SERVICE.TRANSITION_INTERVENE_TYPE_ADD_NODE:
                    transition_name = '加签操作'
                elif ticket_flow_log.intervene_type_id == CONSTANT_SERVICE.TRANSITION_INTERVENE_TYPE_ADD_NODE_END:
                    transition_name = '加签完成操作'
                elif ticket_flow_log.intervene_type_id == CONSTANT_SERVICE.TRANSITION_INTERVENE_TYPE_ACCEPT:
                    transition_name = '接单操作'
                else:
                    transition_name = '未知操作'

            state_info_dict = dict(
                state_id=state_obj.id, state_name=state_obj.name)
            transition_info_dict = dict(
                transition_id=ticket_flow_log.transition_id,
                transition_name=transition_name)
            ticket_flow_log_restful_list.append(
                dict(
                    id=ticket_flow_log.id,
                    ticket_id=ticket_id,
                    state=state_info_dict,
                    transition=transition_info_dict,
                    intervene_type_id=ticket_flow_log.intervene_type_id,
                    participant=ticket_flow_log.participant,
                    participant_type_id=ticket_flow_log.participant_type_id,
                    suggestion=ticket_flow_log.suggestion,
                    gmt_created=str(ticket_flow_log.gmt_created)[:19],
                    gmt_modified=str(ticket_flow_log.gmt_modified)[:19],
                ))
        return ticket_flow_log_restful_list, dict(
            per_page=per_page, page=page, total=paginator.count)

    @classmethod
    @auto_log
    def get_ticket_flow_step(cls, ticket_id, username):
        """

        :param ticket_id:
        :param username:
        :return:
        """
        ticket_obj = TicketRecord.objects.filter(id=ticket_id, is_deleted=0).first()
        if not ticket_obj:
            return False, "工单不存在或已被删除"
        workflow_id = ticket_obj.workflow_id
        state_objs, msg = WorkflowStateService.get_workflow_states(workflow_id)
        ticket_flow_log_queryset = TicketFlowLog.objects.filter(
            ticket_id=ticket_id, is_deleted=0).all()

        state_step_dict_list = []
        for state_obj in state_objs:
            if state_obj.id == ticket_obj.state_id or (not state_obj.is_hidden):
                ticket_state_step_dict = dict(
                    state_id=state_obj.id,
                    state_name=state_obj.name,
                    order_id=state_obj.order_id)
                if state_obj.id <= ticket_obj.state_id:
                    ticket_state_step_dict['is_deal'] = True
                else:
                    ticket_state_step_dict['is_deal'] = False
                state_flow_log_list = []
                for ticket_flow_log in ticket_flow_log_queryset:
                    # 流转记录状态与该状态一致
                    if ticket_flow_log.state_id == state_obj.id:
                        if ticket_flow_log.transition_id:
                            transition_obj, msg = WorkflowTransitionService.get_workflow_transition_by_id(
                                ticket_flow_log.transition_id)
                            transition_name = transition_obj.name
                        else:
                            if ticket_flow_log.intervene_type_id == CONSTANT_SERVICE.TRANSITION_INTERVENE_TYPE_DELIVER:
                                transition_name = '转交操作'
                            elif ticket_flow_log.intervene_type_id == CONSTANT_SERVICE.TRANSITION_INTERVENE_TYPE_ADD_NODE:
                                transition_name = '加签操作'
                            elif ticket_flow_log.intervene_type_id == CONSTANT_SERVICE.TRANSITION_INTERVENE_TYPE_ADD_NODE_END:
                                transition_name = '加签完成操作'
                            elif ticket_flow_log.intervene_type_id == CONSTANT_SERVICE.TRANSITION_INTERVENE_TYPE_ACCEPT:
                                transition_name = '接单操作'
                            else:
                                transition_name = '未知操作'
                        state_flow_log_list.append(
                            dict(
                                id=ticket_flow_log.id,
                                transition=dict(
                                    transition_name=transition_name,
                                    transition_id=ticket_flow_log.transition_id),
                                participant_type_id=ticket_flow_log.participant_type_id,
                                participant=ticket_flow_log.participant,
                                intervene_type_id=ticket_flow_log.intervene_type_id,
                                suggestion=ticket_flow_log.suggestion,
                                state_id=ticket_flow_log.state_id,
                                gmt_created=str(ticket_flow_log.gmt_created)[:19]))
                ticket_state_step_dict['state_flow_log_list'] = state_flow_log_list
                state_step_dict_list.append(ticket_state_step_dict)
        return state_step_dict_list, ''

    @classmethod
    @auto_log
    def update_ticket_state(cls, ticket_id, state_id, username):
        """
        更新工单状态id, 不考虑目标状态处理人及类型为脚本、变量等情况
        :param ticket_id:
        :param state_id:
        :param username:
        :return:
        """
        ticket_obj = TicketRecord.objects.filter(
            id=ticket_id, is_deleted=0).first()
        if not ticket_obj:
            return False, "工单不存在或已被删除"
        source_state_id = ticket_obj.state_id
        state_obj, msg = WorkflowStateService.get_workflow_state_by_id(
            state_id)
        if not state_obj:
            return False, msg

        if state_obj.workflow_id == ticket_obj.workflow_id:
            ticket_obj.state_id = state_id
            ticket_obj.participant_type_id = state_obj.participant_type_id
            ticket_obj.participant = state_obj.participant
            ticket_obj.modifier = username
            ticket_obj.save()

            cls.add_ticket_flow_log(
                dict(
                    ticket_id=ticket_id,
                    transition_id=0,
                    suggestion="强制修改工单状态",
                    participant_type_id=CONSTANT_SERVICE.PARTICIPANT_TYPE_PERSONAL,
                    participant=username,
                    state_id=source_state_id))

            return True, "修改工单状态成功"
        else:
            return False, "修改状态与工单不属于同个工作流"

    @classmethod
    @auto_log
    def accept_ticket(cls, ticket_id, username):
        # 判断权限
        permission, msg = ticket_handle_permission_check(
            ticket_id, username)
        if not permission:
            return False, msg
        if msg['need_accept']:
            new_relation, msg = cls.add_ticket_relation(ticket_id, username)
            ticket_obj = TicketRecord.objects.filter(
                id=ticket_id, is_deleted=0).first()
            ticket_obj.participant_type_id = CONSTANT_SERVICE.PARTICIPANT_TYPE_PERSONAL
            ticket_obj.participant = username
            ticket_obj.modifier = username
            ticket_obj.save()

            ticket_flow_log_dict = dict(
                ticket_id=ticket_id,
                transition=0,
                suggestion='接单处理',
                participant_type_id=CONSTANT_SERVICE.PARTICIPANT_TYPE_PERSONAL,
                participant=username,
                intervene_type_id=CONSTANT_SERVICE.
                    TRANSITION_INTERVENE_TYPE_ACCEPT,
                state_id=ticket_obj.state_id,
                creator=username)
            cls.add_ticket_flow_log(ticket_flow_log_dict)
            return True, "接单成功"
        else:
            return False, "工单当前实际处理人只有一个, 无需先接单"

    @classmethod
    @auto_log
    def deliver_ticket(cls, ticket_id, username, target_username, suggestion):
        """
        转交工单
        :param ticket_id:
        :param username:
        :param target_username:
        :param suggestion:
        :return:
        """
        permission, msg = ticket_handle_permission_check(
            ticket_id, username)
        if not permission:
            return False, msg
        user_obj, msg = AccountBaseService.get_user_by_username(
            target_username)
        if not user_obj:
            return False, "转交用户不存在"

        cls.add_ticket_relation(ticket_id, target_username)
        ticket_obj = TicketRecord.objects.filter(
            id=ticket_id, is_deleted=0).first()
        ticket_obj.participant_type_id = CONSTANT_SERVICE.PARTICIPANT_TYPE_PERSONAL
        ticket_obj.participant = target_username
        ticket_obj.modifier = username
        ticket_obj.save()
        ticket_flow_log_dict = dict(
            ticket_id=ticket_id,
            transition_id=0,
            suggestion=suggestion,
            participant_type_id=CONSTANT_SERVICE.PARTICIPANT_TYPE_PERSONAL,
            intervene_type_id=CONSTANT_SERVICE.
                TRANSITION_INTERVENE_TYPE_DELIVER,
            participant=username,
            state_id=ticket_obj.state_id,
            creator=username)
        cls.add_ticket_flow_log(ticket_flow_log_dict)
        return True, ''

    @classmethod
    @auto_log
    def add_node_ticket(cls, ticket_id, username, target_username, suggestion):
        """
        加签操作
        :param ticket_id:
        :param username:
        :param target_username:
        :param suggestion:
        :return:
        """
        permission, msg = ticket_handle_permission_check(
            ticket_id, username)
        if not permission:
            return False, msg
        user_obj, msg = AccountBaseService.get_user_by_username(
            target_username)
        if not user_obj:
            return False, "加签用户不存在"

        cls.add_ticket_relation(ticket_id, target_username)
        ticket_obj = TicketRecord.objects.filter(
            id=ticket_id, is_deleted=0).first()
        ticket_obj.participant_type_id = CONSTANT_SERVICE.PARTICIPANT_TYPE_PERSONAL
        ticket_obj.participant = target_username
        ticket_obj.in_add_node = True
        ticket_obj.add_node_man = username
        ticket_obj.modifier = username
        ticket_obj.save()
        # 记录处理日志
        ticket_flow_log_dict = dict(
            ticket_id=ticket_id,
            transition_id=0,
            suggestion=suggestion,
            participant_type_id=CONSTANT_SERVICE.PARTICIPANT_TYPE_PERSONAL,
            intervene_type_id=CONSTANT_SERVICE.
                TRANSITION_INTERVENE_TYPE_ADD_NODE,
            participant=username,
            state_id=ticket_obj.state_id,
            creator=username)
        cls.add_ticket_flow_log(ticket_flow_log_dict)
        return True, ''

    @classmethod
    @auto_log
    def add_node_ticket_end(cls, ticket_id, username, suggestion):
        """
        加签工单完成
        :param ticket_id:
        :param username:
        :param suggestion:
        :return:
        """
        permission, msg = ticket_handle_permission_check(
            ticket_id, username)
        if not permission:
            return False, msg
        ticket_obj = TicketRecord.objects.filter(
            id=ticket_id, is_deleted=0).first()
        ticket_obj.participant_type_id = CONSTANT_SERVICE.PARTICIPANT_TYPE_PERSONAL
        ticket_obj.participant = ticket_obj.add_node_man
        ticket_obj.in_add_node = False
        ticket_obj.add_node_man = ''
        ticket_obj.modifier = username
        ticket_obj.save()
        # 记录处理日志
        ticket_flow_log_dict = dict(
            ticket_id=ticket_id,
            transition_id=0,
            suggestion=suggestion,
            participant_type_id=CONSTANT_SERVICE.PARTICIPANT_TYPE_PERSONAL,
            intervene_type_id=CONSTANT_SERVICE.
                TRANSITION_INTERVENE_TYPE_ADD_NODE_END,
            participant=username,
            state_id=ticket_obj.state_id,
            creator=username)
        cls.add_ticket_flow_log(ticket_flow_log_dict)
        return True, ''

    @classmethod
    @auto_log
    def ticket_delete(cls, username, delete_str):
        """
        删除工单
        :param username:
        :param delete_str:
        :return:
        """
        # 去重 and 去空
        delete_set = set(delete_str.split(','))
        delete_list = [int(delete_id) for delete_id in delete_set if delete_id]

        permission = admin_permission_check(username)
        if not permission:
            return False, "用户权限不够"

        deleted_list = []
        ticket_objs = TicketRecord.objects.filter(
            pk__in=delete_list, is_deleted=False)
        if not ticket_objs:
            return False, "删除工单id不存在"
        for ticket_obj in ticket_objs:
            ticket_obj.is_deleted = True
            ticket_obj.modifier = username
            deleted_list.append(str(ticket_obj.id))
            ticket_obj.save()
            cls.add_ticket_flow_log(
                dict(
                    ticket_id=ticket_obj.id,
                    transition_id=0,
                    suggestion="删除工单操作",
                    participant_type_id=CONSTANT_SERVICE.PARTICIPANT_TYPE_PERSONAL,
                    participant=username,
                    state_id=ticket_obj.state_id,
                    creator=username))

        deleted_str = ','.join(deleted_list)
        return deleted_str, ''

    @classmethod
    @auto_log
    def async_diy_field(cls, username, ticket_id, request_data_dict):

        if request_data_dict.__contains__('application_detail'):
            application_detail = request_data_dict.get('application_detail', '')
            if not application_detail:
                return False, '工单无电路详情信息'
            try:
                app_detail_list = json.loads(application_detail)
                app_detail_list = (detail for detail in app_detail_list if detail)
                index = 1
                for detail in app_detail_list:

                    # 过滤修改某些特殊字段
                    detail['ticket_id'] = ticket_id
                    detail['field_num'] = index
                    building_a, building_z = detail.setdefault('building_A', ''), detail.setdefault('building_Z', '')
                    room_a, room_z = detail.setdefault('room_A', ''), detail.setdefault('room_Z', '')
                    if building_a and room_a:
                        fk_rid_a = BuildingRoomInfo.objects.filter(room=room_a,
                                                                   building_info__building=building_a,
                                                                   is_deleted=0).first()
                        detail['fk_rid_A'] = fk_rid_a.id if fk_rid_a else 0
                    else:
                        detail['fk_rid_A'] = 0
                    if building_z and room_z:
                        fk_rid_z = BuildingRoomInfo.objects.filter(room=room_z,
                                                                   building_info__building=building_z,
                                                                   is_deleted=0).first()
                        detail['fk_rid_Z'] = fk_rid_z.id if fk_rid_z else 0
                    else:
                        detail['fk_rid_Z'] = 0
                    del detail['building_A']
                    del detail['building_Z']
                    del detail['room_A']
                    del detail['room_Z']

                    detail = dict(filter(lambda x: x[1], detail.items()))

                    detail_obj = ApplicationDetail.objects.filter(
                        ticket_id=ticket_id, field_num=index).first()
                    if not detail_obj:
                        detail_obj = ApplicationDetail.objects.create(**detail)
                    else:
                        ApplicationDetail.objects.filter(
                            ticket_id=ticket_id,
                            field_num=index).update(**detail)
                    index += 1
                    if not detail_obj:
                        return False, "同步自定义字段 application_detail 失败 "

                    route_info = detail.get('route_info', {})
                    route_first = route_info.setdefault('first', '')
                    route_second = route_info.setdefault('second', '')
                    # 生成 circuit_num
                    route_objs = RouteInfo.objects.filter(application_detail=detail_obj, is_deleted=0).all()
                    if route_objs.first():
                        # 如果路由信息存在且没有变化，则跳过。否则覆盖
                        ofiber_first_list = [str(i.ofiber_core_id) for i in route_objs.filter(route_no='first') if i]
                        ofiber_second_list = [str(i.ofiber_core_id) for i in route_objs.filter(route_no='second') if i]
                        if ','.join(ofiber_first_list) == route_first and ','.join(ofiber_second_list) == route_second:
                            continue

                        circuit_num = route_objs.first().circuit_num
                        RouteInfo.objects.filter(application_detail=detail_obj, circuit_num=circuit_num).delete()
                    else:
                        circuit_num = RouteInfo.objects.all().aggregate(Max('circuit_num')).get('circuit_num__max')
                        if circuit_num:
                            circuit_num = "F" + str(int(circuit_num[1:]) + 1)
                        else:
                            circuit_num = "F0001"

                    if route_first:
                        ofiber_id_list = route_first.split(',')
                        for i in range(len(ofiber_id_list)):
                            RouteInfo.objects.create(circuit_num=circuit_num,
                                                     route_no='first',
                                                     route_where=i + 1,
                                                     state="在用",
                                                     creator=username,
                                                     modifier=username,
                                                     application_detail_id=detail_obj.id,
                                                     ofiber_core_id=ofiber_id_list[i])
                    if route_second:
                        ofiber_id_list = route_second.split(',')
                        for i in range(len(ofiber_id_list)):
                            RouteInfo.objects.create(circuit_num=circuit_num,
                                                     route_no='second',
                                                     route_where=i + 1,
                                                     state="在用",
                                                     creator=username,
                                                     modifier=username,
                                                     application_detail_id=detail_obj.id,
                                                     ofiber_core_id=ofiber_id_list[i])

            except JSONDecodeError as err:
                return False, err

        return True, ''

    @classmethod
    @auto_log
    def get_ticket_dest_relation(cls, destination_participant_type_id,
                                 destination_participant):
        if destination_participant_type_id in (
                CONSTANT_SERVICE.PARTICIPANT_TYPE_PERSONAL,
                CONSTANT_SERVICE.PARTICIPANT_TYPE_MULTI):
            add_relation = destination_participant
        elif destination_participant_type_id == CONSTANT_SERVICE.PARTICIPANT_TYPE_DEPT:
            username_list, msg = AccountBaseService.get_dept_username_list(
                int(destination_participant))
            add_relation = ','.join(username_list)
        elif destination_participant_type_id == CONSTANT_SERVICE.PARTICIPANT_TYPE_ROLE:
            username_list, msg = AccountBaseService.get_role_username_list(
                int(destination_participant))
            add_relation = ','.join(username_list)
        else:
            add_relation = ''
        return add_relation, ''
