#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date: 2018/7/26 12:22

from backend.account import views

__author__ = 'x-zj'

from django.conf.urls import url

app_name = 'account'

urlpatterns = [
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^account_change/$', views.account_change, name='account_change'),
    url(r'^password_change/$', views.password_change, name='password_change'),
    url(r'^get_token/$', views.get_token, name='get_token'),
]
