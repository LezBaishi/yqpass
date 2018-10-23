#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date: 2018/9/4 14:47
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "yuanqu2.settings")
django.setup()

from backend.ticket.models import TicketRecord

__author__ = 'x-zj'

ticket_id = globals().get("ticket_id", '')
ticket_obj = TicketRecord.objects.filter(ticket_id=ticket_id, is_deleted=False).first()
