# !/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import absolute_import
from celery import Celery, platforms
platforms.C_FORCE_ROOT = True  # 加上这一行
app = Celery('celery_pro', include=['celery_pro.tasks'])

app.config_from_object('celery_pro.config')

if __name__ == '__main__':
    app.start()
