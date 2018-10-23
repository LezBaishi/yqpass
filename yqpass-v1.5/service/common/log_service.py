#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date: 2018/6/1 10:46
import functools
import logging
import traceback

__author__ = 'x-zj'

logger = logging.getLogger('django')


def auto_log(func):
    """
    记录日志的装饰器
    :param func:
    :return:
    """

    @functools.wraps(func)
    def _deco(*args, **kwargs):
        try:
            real_func = func(*args, **kwargs)
            return real_func
        except Exception as e:
            logger.error(traceback.format_exc())
            return False, e.__str__()

    return _deco
