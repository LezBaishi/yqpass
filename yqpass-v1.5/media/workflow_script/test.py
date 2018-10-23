#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date: 2018-07-20 23:32:00

import os

from backend.ticket.models import TicketRecord

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "yuanqu2.settings")
import django

django.setup()
__author__ = 'x-zj'


ticket_obj = TicketRecord.objects.all()[0]
ticket_obj.title = "测试工单00001"
ticket_obj.save()
print(ticket_obj.__dict__)
print("test script.py")
print(globals().get("ticket_id", "meiyou"))
