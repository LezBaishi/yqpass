#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date: 2018/8/6 16:29
import json

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from backend.workflow.models import State
from service.common.base_services import BaseService
from service.common.constant_service import CONSTANT_SERVICE
from service.common.log_service import auto_log
from service.workflow.transition_service import WorkflowTransitionService
from service.workflow.custom_field_service import WorkflowCustomFieldService

__author__ = 'x-zj'


class WorkflowStateService(BaseService):

    def __init__(self):
        pass

    @classmethod
    @auto_log
    def get_workflow_init_state(cls, workflow_id):
        """
        获取工作流的初始状态信息, 包括允许的 trasition
        :param workflow_id:
        :return:
        """
        # 获取某个工作流的初始状态
        init_state_obj = State.objects.filter(workflow_id=workflow_id,
                                              is_deleted=0,
                                              type_id=CONSTANT_SERVICE.STATE_TYPE_START).first()
        if not init_state_obj:
            return False, "该工作流不存在或尚未配置初始状态"

        # 通过初始化状态id, 获取后续的各类流转结果。
        # 简化：(source_state_id, destination_state_id)
        # 保存的是 后续状态的流转id和流转name
        transition_queryset, msg = WorkflowTransitionService.get_state_transition_queryset(init_state_obj.id)
        if not transition_queryset:
            return False, msg

        transition_info_list = []
        for transition in transition_queryset:
            transition_info_list.append(dict(transition_id=transition.id, transition_name=transition.name))

        # 工单基础字段及属性
        field_list = []
        field_list.append(dict(field_key='title', name="标题", value=None, order_id=20,
                               field_type_id=CONSTANT_SERVICE.FIELD_TYPE_STR,
                               field_attribute=CONSTANT_SERVICE.FIELD_ATTRIBUTE_RO))

        # 获取工作流中所有的自定义字段。再把每个字段都加到 field_list
        custom_field_dict, msg = WorkflowCustomFieldService.get_workflow_custom_field(workflow_id)
        for key, value in custom_field_dict.items():
            field_list.append(dict(field_key=key,
                                   field_name=custom_field_dict[key]['field_name'],
                                   field_value=None,
                                   order_id=custom_field_dict[key]['order_id'],
                                   field_type_id=custom_field_dict[key]['field_type_id'],
                                   field_attribute=CONSTANT_SERVICE.FIELD_ATTRIBUTE_RO,
                                   field_choice=json.loads(custom_field_dict[key]['field_choice']),
                                   ))

        # 规定字段的权限。"json格式,包括读写属性
        #    1：只读，2：必填，3：可选. 示例："
        #    "{'created_at':1,'title':2, 'sn':1}, "
        #    "内置特殊字段
        #    participant_info.participant_name: 当前处理人信息(部门名称、角色名称)
        #    state.state_name: 当前状态的状态名
        #    workflow.workflow_name: 工作流名称
        state_field_dict = json.loads(init_state_obj.state_field_str)
        state_field_key_list = state_field_dict.keys()

        # 对 field_list 遍历, 找到规定的字段，然后替换权限，加入到新的列表 new_field_list 中
        new_field_list = []
        for field in field_list:
            if field['field_key'] in state_field_key_list:
                field['field_attribute'] = state_field_dict[field['field_key']]
                new_field_list.append(field)

        # 字段排序
        new_field_list = sorted(new_field_list, key=lambda r: r['order_id'])
        state_info_dict = dict(
            id=init_state_obj.id,
            name=init_state_obj.name,
            workflow_id=init_state_obj.workflow_id,
            sub_workflow_id=init_state_obj.sub_workflow_id,
            distribute_type_id=init_state_obj.distribute_type_id,
            is_hidden=init_state_obj.is_hidden,
            order_id=init_state_obj.order_id,
            type_id=init_state_obj.type_id,
            participant_type_id=init_state_obj.participant_type_id,
            participant=init_state_obj.participant,
            field_list=new_field_list,
            label=json.loads(init_state_obj.label),
            creator=init_state_obj.creator,
            gmt_created=str(init_state_obj.gmt_created)[:19],
            transition=transition_info_list
        )

        return state_info_dict, ''

    @classmethod
    def get_restful_state_info_by_id(cls, state_id):
        """
        获取相应状态信息
        :param state_id:
        :return:
        """
        if not state_id:
            return False, "请提供对应的状态id"

        workflow_state = State.objects.filter(id=state_id, is_deleted=0).first()
        if not workflow_state:
            return False, "工单状态不存在或已被删除"
        state_info_dict = dict(id=workflow_state.id,
                               name=workflow_state.name,
                               workflow_id=workflow_state.workflow_id,
                               sub_workflow_id=workflow_state.sub_workflow_id,
                               distribute_type_id=workflow_state.distribute_type_id,
                               is_hidden=workflow_state.is_hidden,
                               order_id=workflow_state.order_id, type_id=workflow_state.type_id,
                               participant_type_id=workflow_state.participant_type_id,
                               participant=workflow_state.participant,
                               state_field=json.loads(workflow_state.state_field_str),
                               label=json.loads(workflow_state.label),
                               creator=workflow_state.creator,
                               gmt_created=str(workflow_state.gmt_created)[:19]
                               )
        return state_info_dict, ''

    @classmethod
    def get_workflow_start_state(cls, workflow_id):
        """
        获取工作流初始状态
        :param workflow_id:
        :return:
        """
        workflow_state_queryset = State.objects.filter(is_deleted=0, workflow_id=workflow_id).all()
        for workflow_state in workflow_state_queryset:
            if workflow_state.type_id == CONSTANT_SERVICE.STATE_TYPE_START:
                return workflow_state, ''
        return False, "该工作流尚未配置初始状态"

    @classmethod
    def get_workflow_state_by_id(cls, state_id):
        """
        :param state_id:
        :return:
        """
        workflow_state = State.objects.filter(id=state_id, is_deleted=0).first()
        if not workflow_state:
            return False, "该工单状态不存在或已被删除"
        return workflow_state, ''

    @classmethod
    @auto_log
    def get_workflow_states(cls, workflow_id):
        """
        获取流程的状态列表。
        :param workflow_id:
        :return:
        """
        if not workflow_id:
            return False, "没有提供 workflow_id"

        workflow_stats = State.objects.filter(workflow_id=workflow_id, is_deleted=0).order_by('order_id')
        if not workflow_stats:
            return False, "该工作流不存在状态信息"
        return workflow_stats, ''

    @classmethod
    @auto_log
    def get_restful_state_list_by_id(cls, workflow_id, per_page, page):
        """

        :param workflow_id:
        :param per_page:
        :param page:
        :return:
        """

        state_objects, msg = cls.get_workflow_states(workflow_id)
        if not state_objects:
            return False, msg

        paginator = Paginator(state_objects, per_page)
        try:
            state_paginator = paginator.page(page)
        except PageNotAnInteger:
            state_paginator = paginator.page(1)
        except EmptyPage:
            state_paginator = paginator.page(paginator.num_pages)

        state_result_object_list = state_paginator.object_list
        state_restful_list = []

        for state in state_result_object_list:
            state_restful_list.append(dict(id=state.id,
                                           name=state.name,
                                           workflow_id=state.workflow_id,
                                           sub_workflow_id=state.sub_workflow_id,
                                           distribute_type_id=state.distribute_type_id,
                                           is_hidden=state.is_hidden,
                                           order_id=state.order_id,
                                           type_id=state.type_id,
                                           participant_type_id=state.participant_type_id,
                                           participant=state.participant,
                                           state_field=json.loads(state.state_field_str),
                                           label=json.loads(state.label),
                                           creator=state.creator,
                                           gmt_created=str(state.gmt_created)[:19]
                                           ))

        return state_restful_list, dict(per_page=per_page, page=page, total=paginator.count)
