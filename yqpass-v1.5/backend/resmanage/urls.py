#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date: 2018/9/4 14:20
from backend.resmanage import views
from django.conf.urls import url

from backend.resmanage.views import *

__author__ = 'mc'
app_name = 'resmanage'

urlpatterns = [
    url(r'^view_test/$', views.mysql_view_test, name='view_test'),
    url(r'^building/$', BuildingListView.as_view()),
    url(r'^building_room/$', BuildingRoomListView.as_view()),
    url(r'^ocable_section/$', OcableSectionListView.as_view()),
    url(r'^(?P<pk>[0-9]+)/ocable_section/$', OcableSectionDetailView.as_view()),
    url(r'^ocable_section/delete/$', OcableSectionDeleteView.as_view()),
    url(r'^ofiber_core/$', OfiberCoreListView.as_view()),
    url(r'^(?P<pk>[0-9]+)/ofiber_core/$', OfiberCoreDetailView.as_view()),
    url(r'^ofiber_core/delete/$', OfiberCoreDeleteView.as_view()),
    url(r'^using_circuit/$', UsingCircuitListView.as_view()),
    url(r'^using_circuit/delete/$', UsingCircuitDeleteView.as_view()),
]
