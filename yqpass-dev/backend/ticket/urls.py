#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date: 2018/8/1 15:32
from django.conf.urls import url

# from backend.ticket.views import TicketListView
from backend.ticket.views import TicketListView, TicketView, TicketTransition, TicketFlowlog, TicketFlowStep, \
    TicketState, TicketAccept, TicketDeliver, TicketAddNode, TicketAddNodeEnd, TicketDelete

__author__ = 'x-zj'

app_name = 'ticket'

urlpatterns = [
    url(r'^$', TicketListView.as_view()),
    url(r'^(?P<pk>[0-9]+)/$', TicketView.as_view()),
    url(r'^(?P<pk>[0-9]+)/transitions/$', TicketTransition.as_view()),
    url(r'^(?P<pk>[0-9]+)/flowlogs/$', TicketFlowlog.as_view()),
    url(r'^(?P<pk>[0-9]+)/flowsteps/$', TicketFlowStep.as_view()),
    url(r'^(?P<pk>[0-9]+)/change_state/$', TicketState.as_view()),
    url(r'^(?P<pk>[0-9]+)/accept/$', TicketAccept.as_view()),
    url(r'^(?P<pk>[0-9]+)/deliver/$', TicketDeliver.as_view()),
    url(r'^(?P<pk>[0-9]+)/add_node/$', TicketAddNode.as_view()),
    url(r'^(?P<pk>[0-9]+)/add_node_end/$', TicketAddNodeEnd.as_view()),
    url(r'^delete/$', TicketDelete.as_view()),
]
