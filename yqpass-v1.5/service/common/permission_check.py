#!usr/bin/env python  
# -*- coding:utf-8 _*-  
""" 
@author: x-zj
@file: permission_check.py 
@version:
@time: 2018/10/9 10:00
"""
from backend.account.models import User
from backend.ticket.models import TicketRecord
from service.account.base_services import AccountBaseService
from service.common.constant_service import CONSTANT_SERVICE
from service.common.log_service import auto_log
from service.workflow.base_services import WorkflowBaseService
from service.workflow.state_service import WorkflowStateService
from service.workflow.transition_service import WorkflowTransitionService


@auto_log
def admin_permission_check(username):
    """
    校验管理员权限
    :param username:
    :return:
    """
    user_obj = User.objects.filter(username=username, is_deleted=0).first()
    if not user_obj:
        return False, "该用户不存在"
    if user_obj.is_staff:
        return True, ''
    else:
        return False, "该用户非管理员"


@auto_log
def check_new_ticket_permission(username, workflow_id):
    user_obj = User.objects.filter(username=username, is_deleted=0).first()
    if not user_obj.is_admin and user_obj.is_viewer:
        return False, ''

    return True, ''


@auto_log
def ticket_handle_permission_check(ticket_id, username):
    """
    处理权限校验: 获取当前状态是否需要处理, 该用户是否有权限处理
    1. 验证是否为参观账号
    2. 验证工单是否存在
    3. 确认工单该状态对应处理人是否包含
    :param ticket_id:
    :param username:
    :return:
    """
    ticket_obj = TicketRecord.objects.filter(
        id=ticket_id, is_deleted=0).first()
    user_obj = User.objects.filter(username=username, is_deleted=0).first()

    if not user_obj.is_admin and user_obj.is_viewer:
        return False, "该账号权限不够"
    if not ticket_obj:
        return False, "工单不存在或已被删除"
    ticket_state_id = ticket_obj.state_id
    transition_queryset, msg = WorkflowTransitionService.get_state_transition_queryset(
        ticket_state_id)
    if not transition_queryset:
        return False, "工单当前状态不需操作"
    state_obj, msg = WorkflowStateService.get_workflow_state_by_id(
        ticket_state_id)
    if not state_obj:
        return False, "工单当前状态id不存在或已被删除"
    participant_type_id = ticket_obj.participant_type_id
    participant = ticket_obj.participant

    # 当前处理人个数, 大于1时 需要先接单再处理
    current_participant_count = 1

    if participant_type_id == CONSTANT_SERVICE.PARTICIPANT_TYPE_PERSONAL:
        if username != participant and not user_obj.is_staff:
            return False, "非当前处理人, 无权处理"
    elif participant_type_id == CONSTANT_SERVICE.PARTICIPANT_TYPE_MULTI:
        if username not in participant.split(
                ',') and not user_obj.is_staff:
            return False, "非当前处理人, 无权处理"
        current_participant_count = len(participant.split(','))
    elif participant_type_id == CONSTANT_SERVICE.PARTICIPANT_TYPE_DEPT:
        dept_user_list, msg = AccountBaseService.get_dept_username_list(
            dept_id=participant)
        if username not in dept_user_list and not user_obj.is_staff:
            return False, "非当前处理人, 无权处理"
        current_participant_count = len(dept_user_list)
    elif participant_type_id == CONSTANT_SERVICE.PARTICIPANT_TYPE_ROLE:
        role_user_list, msg = AccountBaseService.get_role_username_list(
            role_id=participant)
        if username not in role_user_list and not user_obj.is_staff:
            return False, "非当前处理人, 无权处理"
        current_participant_count = len(role_user_list)
    else:
        return False, "非当前处理人, 无权处理"

    if current_participant_count > 1 and state_obj.distribute_type_id == CONSTANT_SERVICE.STATE_DISTRIBUTE_TYPE_ACTIVE:
        need_accept = True
    else:
        need_accept = False
    if ticket_obj.in_add_node:
        in_add_node = True
    else:
        in_add_node = False

    return True, dict(need_accept=need_accept, in_add_node=in_add_node)


@auto_log
def ticket_view_permission_check(ticket_id, username):
    """
    如果是参观账号，都有查看权限
    校验用户有工单的查看权限, 先查看对应的工作流是否有校验查看权限, 如果不校验直接允许, 如果需要校验则判断用户是否属于工单的关系人
    :param ticket_id:
    :param username:
    :return:
    """
    ticket_obj = TicketRecord.objects.filter(
        id=ticket_id, is_deleted=0).first()
    if not ticket_obj:
        return False, "工单不存在或已被删除"
    workflow_obj, msg = WorkflowBaseService.get_by_id(
        ticket_obj.workflow_id)
    if not workflow_obj:
        return False, msg
    user_obj, msg = AccountBaseService.get_user_by_username(username)
    if not user_obj:
        return False, msg
    if not workflow_obj.view_permission_check:
        return True, "该工单不限制查看权限"
    else:
        if username in ticket_obj.relation.split(','):
            return True, "用户是该工单的关系人, 有查看权限"
        elif user_obj.is_staff or user_obj.is_viewer:
            return True, "用户拥有特殊权限, 可查看"
        else:
            return False, "用户不是该工单的关系人, 且该工单开启了查看权限"
