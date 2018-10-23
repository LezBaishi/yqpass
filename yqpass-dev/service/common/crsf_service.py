#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date: 2018/8/10 10:57
from django.utils.deprecation import MiddlewareMixin

__author__ = 'x-zj'


class DisableCSRF(MiddlewareMixin):
    def process_request(self, request):
        if request.path.startswith('/api/'):
            setattr(request, '_dont_enforce_csrf_checks', True)
