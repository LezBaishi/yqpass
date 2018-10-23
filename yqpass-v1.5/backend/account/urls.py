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
    url(r'^user_list/$', views.user_list, name='user_list'),
    url(r'^(?P<pk>[0-9]+)/user_detail/$', views.user_detail, name='user_detail',),
    url(r'^user_delete/$', views.user_delete, name='user_delete'),
    url(r'^role_list/$', views.role_list, name='role_list'),
    url(r'^(?P<pk>[0-9]+)/role_members/$', views.role_members, name='role_members'),
    url(r'^(?P<pk>[0-9]+)/role_detail/$', views.role_detail, name='role_detail', ),
    url(r'^role_delete/$', views.role_delete, name='role_delete'),
    url(r'^dept_list/$', views.dept_list, name='dept_list'),
    url(r'^(?P<pk>[0-9]+)/dept_detail/$', views.dept_detail, name='dept_detail', ),
    url(r'^dept_delete/$', views.dept_delete, name='dept_delete'),

]
