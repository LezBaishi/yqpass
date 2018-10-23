#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date: 2018/8/1 15:37
import datetime

__author__ = 'x-zj'

import json

from django.http import HttpResponse


def api_response(code, msg='', data=''):
    """
    格式化返回
    :param code:
    :param msg:
    :param data:
    :return:
    """

    return HttpResponse(json.dumps(dict(code=code, data=data, msg=msg), ensure_ascii=False),
                        content_type="application/json", charset='utf-8')


class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self, obj)