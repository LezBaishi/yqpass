#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date: 2018/9/5 15:55
from backend.fielddiy.models import ApplicationDetail
from service.common.base_services import BaseService
from service.common.log_service import auto_log

__author__ = 'x-zj'


class FielddiyBaseService(BaseService):

    @classmethod
    @auto_log
    def get_application_detail_by_ticket_id(cls, ticket_id):
        """

        :param ticket_id:
        :return:
        """
        app_details = ApplicationDetail.objects.filter(ticket_id=ticket_id).all().order_by('-field_num')
        if not app_details:
            return False, "该工单不存在申请单明细表"
        app_details_restful_list = []
        for detail in app_details:
            detail_dict = detail.__dict__
            if detail_dict.__contains__('_state'):
                detail_dict.pop('_state')
            app_details_restful_list.append(detail_dict)
        return app_details_restful_list, ''
