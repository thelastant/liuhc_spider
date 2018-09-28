#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import absolute_import

CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/5'
BROKER_URL = 'redis://127.0.0.1:6379/6'

CELERY_TIMEZONE = 'Asia/Shanghai'
from celery.schedules import crontab
from datetime import timedelta

# CELERYD_TASK_TIME_LIMIT = 10  # 单个任务的运行时间不超过此值，否则会被SIGKILL 信号杀死
# 防止死锁
CELERYD_FORCE_EXECV = True
CELERYD_CONCURRENCY = 10
CELERY_TASK_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_RESULT_SERIALIZER = 'json'
# CELERYBEAT_SCHEDULE = 'djcelery.schedulers.DatabaseScheduler'

CELERYBEAT_SCHEDULE = {
    'liu_task': {
        'task': 'celery_pro.tasks.liu_task',
        'schedule': crontab(minute="*/30"),
    },
}
