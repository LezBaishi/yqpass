#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date: 2018/8/14 15:37
import contextlib
import logging
import os
import sys
import traceback

from backend.ticket.models import TicketRecord
from backend.workflow.models import WorkflowScript, Transition, State
from service.account.base_services import AccountBaseService
from service.common.constant_service import CONSTANT_SERVICE
from service.ticket.base_service import TicketBaseService

__author__ = 'x-zj'

from yuanqu2.celery import app
from io import StringIO

logger = logging.getLogger('django')


@app.task
def test_task(a, b):
    print('a={}'.format(1))
    print('b=', b)
    print(a + b)


# 上下文管理、在执行 with 期间，替换 stdout 流
@contextlib.contextmanager
def stdout_io(stdout=None):
    old = sys.stdout
    if stdout is None:
        stdout = StringIO()
    sys.stdout = stdout
    yield stdout
    sys.stdout = old


@app.task
def run_flow_task(ticket_id, script_name, state_id, action_from='robot'):
    """
    执行工作流脚本
    :param script_name:
    :param ticket_id:
    :param state_id:
    :param action_from:
    :return:
    """
    ticket_obj = TicketRecord.objects.filter(id=ticket_id, is_deleted=False).first()
    if ticket_obj.participant == script_name and ticket_obj.participant_type_id == \
            CONSTANT_SERVICE.PARTICIPANT_TYPE_ROBOT:

        # 校验脚本是否合法
        script_obj = WorkflowScript.objects.filter(saved_name='workflow_script/{}'.format(script_name),
                                                   is_deleted=False, is_active=True).first()
        if not script_obj:
            return False, '脚本未注册或非激活状态'

        # script_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "media/workflow_script"))
        script_dir = os.path.abspath(os.path.dirname(__file__))
        script_dir = os.path.abspath(
            os.path.join(os.path.split(os.path.split(script_dir)[0])[0], 'media'))
        script_file = os.path.join(script_dir, script_name)
        globals = {'ticket_id': ticket_id, 'action_from': action_from}
        # 如果需要脚本执行完成后，工单不往下流转(也就脚本执行失败或调用其他接口失败的情况)，需要在脚本中抛出异常
        try:
            with stdout_io() as s:
                # execfile(script_file, globals)  # for python 2
                # https://docs.python.org/3/library/functions.html#exec
                exec(open(script_file, encoding='utf-8').read(), globals)
            script_result = True
            # script_result_msg = ''.join(s.buflist)
            script_result_msg = ''.join(s.getvalue())
            if s:
                s.close()
        except Exception as e:
            logger.error(traceback.format_exc())
            script_result = False
            script_result_msg = e.__str__()
            logger.info('*' * 20 + '工作流脚本回调,ticket_id:[%s]' % ticket_id + '*' * 20)
            logger.info('*******工作流脚本回调，ticket_id:{}*****'.format(ticket_id))

        # 因为上面的脚本执行时间可能会比较长，为了避免db session失效，重新获取ticket对象
        ticket_obj = TicketRecord.objects.filter(id=ticket_id, is_deleted=False).first()
        # 新增处理记录,脚本后只允许只有一个后续直连状态
        transition_obj = Transition.objects.filter(source_state_id=state_id, is_deleted=False).first()
        new_ticket_flow_dict = dict(ticket_id=ticket_id, transition_id=transition_obj.id,
                                    suggestion=script_result_msg,
                                    participant_type_id=CONSTANT_SERVICE.PARTICIPANT_TYPE_ROBOT,
                                    participant=script_name, state_id=state_id, creator='robot')

        TicketBaseService.add_ticket_flow_log(new_ticket_flow_dict)
        if not script_result:
            # 脚本执行失败，状态不更新
            return False, script_result_msg
        # 自动执行流转
        destination_participant = None
        destination_participant_type_id = None
        tar_state_obj = State.objects.filter(id=transition_obj.destination_state_id, is_deleted=False).first()
        add_relation = ''
        if tar_state_obj.participant_type_id == CONSTANT_SERVICE.PARTICIPANT_TYPE_VARIABLE:
            if tar_state_obj.participant == 'creator':
                destination_participant_type_id = CONSTANT_SERVICE.PARTICIPANT_TYPE_PERSONAL
                destination_participant = ticket_obj.creator
                add_relation = destination_participant
            elif tar_state_obj.participant == 'creator_tl':
                approver, msg = AccountBaseService.get_user_dept_approver(ticket_obj.creator)
                if len(approver.split(',')) > 1:
                    destination_participant_type_id = CONSTANT_SERVICE.PARTICIPANT_TYPE_MULTI
                else:
                    destination_participant_type_id = CONSTANT_SERVICE.PARTICIPANT_TYPE_PERSONAL
                destination_participant = approver
                add_relation = destination_participant
        elif tar_state_obj.participant_type_id == CONSTANT_SERVICE.PARTICIPANT_TYPE_FIELD:
            destination_participant, msg = TicketBaseService.get_ticket_field_value(ticket_id,
                                                                                    tar_state_obj.participant)
            destination_participant_type_id = CONSTANT_SERVICE.PARTICIPANT_TYPE_PERSONAL
            if len(destination_participant.split(',')) > 1:
                destination_participant_type_id = CONSTANT_SERVICE.PARTICIPANT_TYPE_MULTI
            add_relation = destination_participant
        elif tar_state_obj.participant_type_id == CONSTANT_SERVICE.PARTICIPANT_TYPE_PARENT_FIELD:
            parent_ticket_id = ticket_obj.parent_ticket_id
            destination_participant, msg = TicketBaseService.get_ticket_field_value(parent_ticket_id,
                                                                                    tar_state_obj.participant)
            destination_participant_type_id = CONSTANT_SERVICE.PARTICIPANT_TYPE_PERSONAL
            if len(destination_participant.split(',')) > 1:
                destination_participant_type_id = CONSTANT_SERVICE.PARTICIPANT_TYPE_MULTI
            add_relation = destination_participant

        else:
            destination_participant_type_id = tar_state_obj.participant_type_id
            destination_participant = tar_state_obj.participant
            if tar_state_obj.participant_type_id == CONSTANT_SERVICE.PARTICIPANT_TYPE_DEPT:
                username_list, msg = AccountBaseService.get_dept_username_list(int(destination_participant))
                add_relation = ','.join(username_list)
            elif tar_state_obj.participant_type_id == CONSTANT_SERVICE.PARTICIPANT_TYPE_ROLE:
                username_list, msg = AccountBaseService.get_role_username_list(int(destination_participant))
                add_relation = ','.join(username_list)
            else:
                add_relation = ''

        # else:
        #     # 其他类型不换算成实际的处理人
        #     destination_participant_type_id = tar_state_obj.participant_type_id
        #     destination_participant = tar_state_obj.participant

        new_ralation, msg = TicketBaseService.add_ticket_relation(ticket_id, add_relation)
        # 记得刷新记录
        ticket_obj = TicketRecord.objects.filter(id=ticket_id, is_deleted=False).first()
        ticket_obj.participant = destination_participant
        ticket_obj.participant_type_id = destination_participant_type_id
        ticket_obj.state_id = tar_state_obj.id
        ticket_obj.save()
        logger.info('******脚本执行成功,工单基础信息更新完成, ticket_id:{}******'.format(ticket_id))

        # 子工单处理
        if tar_state_obj.type_id == CONSTANT_SERVICE.STATE_TYPE_END:
            if ticket_obj.parent_ticket_id:
                sub_ticket_queryset = TicketRecord.objects.filter(parent_ticket_id=ticket_obj.parent_ticket_id,
                                                                  is_deleted=False)
                sub_ticket_state_id_list = []
                for sub_ticket_query0 in sub_ticket_queryset:
                    sub_ticket_state_id_list.append(sub_ticket_query0.state_id)
                if set(sub_ticket_state_id_list) == {ticket_obj.state_id}:
                    # 父工单的所有子工单都已处理结束,自动流转父工单
                    parent_ticket_obj = TicketRecord.objects.filter(id=ticket_obj.parent_ticket_id,
                                                                    is_deleted=False).first()
                    parent_transition_obj = Transition.objects.filter(source_state_id=parent_ticket_obj.state_id,
                                                                      is_deleted=False).first()
                    flag, msg = TicketBaseService.handle_ticket(parent_ticket_obj.id,
                                                                dict(username='robot',
                                                                     suggestion='所有子工单都已结束，自动流转',
                                                                     transition_id=parent_transition_obj.id))
                    if not flag:
                        return True, msg
        # 下个状态也是脚本处理
        if tar_state_obj.participant_type_id == CONSTANT_SERVICE.PARTICIPANT_TYPE_ROBOT:
            run_flow_task.apply_async(args=[ticket_id, tar_state_obj.participant, tar_state_obj.id], queue='yqpass')
        return True, ''
    else:
        return False, '工单当前处理人为非脚本，不执行脚本'
