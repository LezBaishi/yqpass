#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date: 2018/8/14 15:21
from __future__ import absolute_import, unicode_literals

__author__ = 'x-zj'

import os
from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yuanqu2.settings')

app = Celery('yuanqu2')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))