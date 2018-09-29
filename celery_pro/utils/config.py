# coding:utf-8      __author__='python'
import logging
from logging.handlers import RotatingFileHandler
import redis

class config:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://lsh:a123456@45.249.247.90:4040/bbs"
    SQLALCHEMY_BINDS = {
        'cp': 'mysql+pymysql://lsh:a123456@45.249.247.90:4040/caipiao',
    }
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_POOL_SIZE = 20
    # REDIS_HOST = "45.63.51.252" # 暂时用我的服务器测试
    REDIS_HOST = "47.98.232.95"  # 暂时用我的服务器测试
    REDIS_PORT = 6379
    SECRET_KEY = "hello"
    RESTFUL_JSON = dict(ensure_ascii=False)
    JSON_AS_ASCII = False
    SESSION_TYPE = "redis"
    SESSION_USE_SIGNER = True
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)
    PERMANENT_SESSION_LIFETIME = 86400

    # # 爬取图片所用到的数据库
    # SPIDER_HOST = "45.249.247.90"
    # SPIDER_USER = "lsh"
    # SPIDER_PASSWORD = "a123456"
    # SPIDER_DB = "bbs"
    # SPIDER_PORT = 4040
    # 爬取图片所用到的数据库
    SPIDER_HOST = "45.63.51.252"
    SPIDER_USER = "root"
    SPIDER_PASSWORD = "123456"
    SPIDER_DB = "picture"
    SPIDER_PORT = 3306

    # 存入七牛的需要填写你的 Access Key 和 Secret Key 以及上传空间
    spider_access_key = 'ZTby-Y5XJQQdwZBNxqXexw_EH6EeBYeMGKJpEeKg'
    spider_secret_key = 'aT2AZ_yXVXAVZ0aR0JtVrTU7jbbd8hppFn9wZ41Z'
    # 要上传的空间
    spider_bucket_name = 'windlad025'
