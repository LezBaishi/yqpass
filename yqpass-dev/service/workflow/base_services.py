#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date: 2018/8/6 15:09
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q

from backend.workflow.models import Workflow
from service.common.base_services import BaseService
from service.common.log_service import auto_log

__author__ = 'x-zj'


class WorkflowBaseService(BaseService):
    """
    工单流程服务
    """

    def __init__(self):
        pass

    @classmethod
    def get_workflow_list(cls, name, page, per_page):
        """
        获取工作流列表
        :param name:
        :param page:
        :param per_page:
        :return:
        """
        # 构造查询参数
        query_params = Q(is_deleted=0)
        if name:
            query_params &= Q(name__contains=name)
        workflow_queryset = Workflow.objects.filter(query_params).order_by('id')

        # 分页
        paginator = Paginator(workflow_queryset, per_page)
        try:
            workflow_result_paginator = paginator.page(page)
        except PageNotAnInteger:
            workflow_result_paginator = paginator.page(1)
        except EmptyPage:
            workflow_result_paginator = paginator.page(paginator.num_pages)

        workflow_result_object_list = workflow_result_paginator.object_list
        workflow_result_restful_list = []
        for workflow_result_object in workflow_result_object_list:
            workflow_result_restful_list.append(dict(id=workflow_result_object.id,
                                                     name=workflow_result_object.name,
                                                     description=workflow_result_object.description,
                                                     creator=workflow_result_object.creator,
                                                     gmt_created=str(workflow_result_object.gmt_created)[:19]))
        return workflow_result_restful_list, dict(per_page=per_page, page=page, total=paginator.count)

    @classmethod
    @auto_log
    def get_by_id(cls, workflow_id):
        """
        通过id获取工作流
        :param workflow_id:
        :return:
        """
        workflow_object = Workflow.objects.filter(id=workflow_id, is_deleted=0).first()
        if not workflow_object:
            return False, "该工作流不存在"
        return workflow_object, ''

    @classmethod
    @auto_log
    def check_new_permission(cls, username, workflow_id):
        return True, ''
