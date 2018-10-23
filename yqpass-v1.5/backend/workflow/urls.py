#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date: 2018/8/1 15:33
from django.conf.urls import url

from backend.workflow.views import WorkflowView, WorkflowInitView, StateView, StateListView

__author__ = 'x-zj'

app_name = 'workflow'

urlpatterns = [
    url(r'^$', WorkflowView.as_view()),
    url(r'^(?P<pk>[0-9]+)/init_state/$', WorkflowInitView.as_view()),
    url(r'^(?P<pk>[0-9]+)/states_list/$', StateListView.as_view()),
    url(r'^(?P<pk>[0-9]+)/state/$', StateView.as_view()),
]
