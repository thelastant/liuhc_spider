#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import absolute_import
from celery_pro.celery import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from celery_pro.spider.getPictureData import GetPictureData

engine = create_engine("mysql+pymysql://lsh:a123456@45.249.247.90:4040/bbs")
Session = sessionmaker(bind=engine)
Base = declarative_base()

session = Session()


@app.task
def liu_task():
    # # 测试！！！！！！！！！！
    obj = GetPictureData()
    obj.run()

@app.task
def new_liu_task():
    # # 测试！！！！！！！！！！
    obj = GetPictureData()
    obj.run()
