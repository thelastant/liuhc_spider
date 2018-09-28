# -*- coding: utf-8 -*-

import logging
from qiniu import Auth, put_data
from celery_pro.utils.config import config


def storage(data):
    """七牛云存储上传文件接口"""
    if not data:
        return None
    try:
        # 构建鉴权对象
        q = Auth(config.spider_access_key, config.spider_secret_key)

        # 生成上传 Token，可以指定过期时间等
        token = q.upload_token(config.spider_bucket_name)

        # 上传文件
        ret, info = put_data(token, None, data)

    except Exception as e:
        # logging.error(e)
        raise e

    if info and info.status_code != 200:
        raise Exception("上传文件到七牛失败")

    # 返回七牛中保存的图片名，这个图片名也是访问七牛获取图片的路径
    return ret["key"]


def run_save_img(img_num, img_data):
    file_name = str(img_num) + ".jpg"
    if img_num == 15:
        file_name = str(img_num) + ".gif"

    # 图片存入本地
    with open("picture/" + file_name, "wb") as f:
        f.write(img_data)
    f.close()

    # 图片存入到七牛
    with open("picture/" + file_name, "rb") as f:
        src = storage(f.read())
    f.close()
    print(file_name, "图片存入七牛成功")
    return src
