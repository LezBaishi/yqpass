#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date: 2018/9/3 16:27
from backend.ticket.models import TicketCustomField
from service.common.base_services import BaseService
from service.common.log_service import auto_log

__author__ = 'x-zj'


class PickCustomField(BaseService):

    def __init__(self):
        pass

    @classmethod
    @auto_log
    def get_application_detail(cls, ticket_id):
        """
        获取工单中申请明细表详情
        :return:
        """
        custom_fields = TicketCustomField.objects.filter(ticket_id=ticket_id,
                                                         field_key='application_detail',
                                                         is_deleted=False).all()
        if not custom_fields:
            return [], "该工单暂无明细表"
        return custom_fields, len(custom_fields)

