#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View

from service.common.format_response import api_response
from service.workflow.base_services import WorkflowBaseService
from service.workflow.state_service import WorkflowStateService


class WorkflowView(View):

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        """
        获取工作流列表
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        request_data = request.GET
        workflow_name = request_data.get('name', '')
        username = request.user.username

        per_page = int(request_data.get('per_page', 10))
        page = int(request_data.get('page', 1))

        workflow_result_restful_list, msg = WorkflowBaseService.get_workflow_list(workflow_name,
                                                                                  page,
                                                                                  per_page)
        if workflow_result_restful_list is not False:
            data = dict(value=workflow_result_restful_list,
                        per_page=msg['per_page'],
                        page=msg['page'],
                        total=msg['total'])
            code, msg = 1, ''
        else:
            code, data = 0, ''
        return api_response(code, msg, data)


class WorkflowInitView(View):

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        """
        获取工作流初始状态, 包括状态详情以及允许的transition
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        workflow_id = kwargs.get('pk', '')
        request_data = request.GET
        username = request.user.username
        if not workflow_id:
            return api_response(0, "请提供工作流id", '')

        state_result, msg = WorkflowStateService.get_workflow_init_state(workflow_id)
        if state_result is False:
            code, msg, data = 0, msg, ''
        else:
            code, msg, data = 1, msg, state_result

        return api_response(code, msg, data)


class StateView(View):

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        """
        获取状态详情
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        state_id = kwargs.get('pk', '')
        request_data = request.GET
        username = request.user.username

        result, msg = WorkflowStateService.get_restful_state_info_by_id(state_id)
        if result is False:
            code, data = 0, ''
        else:
            code, data = 1, result

        return api_response(code, msg, data)
