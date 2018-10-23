#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date: 2018/7/27 0:04
from django.contrib import admin

from service.common.log_service import auto_log

__author__ = 'x-zj'


class BaseService(object):
    pass


class ModelBaseAdmin(admin.ModelAdmin):
    list_display = ('creator', 'is_deleted', 'gmt_created', 'gmt_modified')
    readonly_fields = ['creator']

    def save_model(self, request, obj, form, change):
        if not obj.creator:
            obj.creator = request.user.username
        obj.save()


@auto_log
def init_django_env():
    import os
    import django

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "yuanqu2.settings")
    django.setup()
