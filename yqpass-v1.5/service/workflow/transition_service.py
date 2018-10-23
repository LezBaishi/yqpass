#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date: 2018/8/6 16:44
from backend.workflow.models import Transition
from service.common.base_services import BaseService
from service.common.log_service import auto_log

__author__ = 'x-zj'


class WorkflowTransitionService(BaseService):

    @classmethod
    @auto_log
    def get_state_transition_queryset(cls, state_id):
        """
        获取状态可以执行的操作
        :param state_id:
        :return:
        """
        destination_transition_queryset = Transition.objects.filter(is_deleted=0, source_state_id=state_id).all()
        if not destination_transition_queryset:
            return False, "没有后续流转流程"
        return destination_transition_queryset, ''

    @classmethod
    def get_workflow_transition_by_id(cls, transition_id):
        workflow_transition = Transition.objects.filter(is_deleted=0, id=transition_id).first()
        if not workflow_transition:
            return False, "请提供正确的 transition_id."
        return workflow_transition, ''
