import re

import requests
import time
from lxml import etree
import pymysql

from celery_pro.utils.config import config


class LihHeSpider(object):
    def __init__(self):
        self.db = pymysql.connect(host=config.SPIDER_HOST, user=config.SPIDER_USER,
                                  password=config.SPIDER_PASSWORD, db=config.SPIDER_DB, port=config.SPIDER_PORT)

    def get_picture(self):
        for i in range(1, 67):
            main_url = "http://www.9343b.com/bbs/ct"
            main_url += "00" + str(i) + ".html" if i < 10 else "0" + str(i) + ".html"
            response = requests.get(url=main_url)
            data = etree.HTML(response.text.encode(response.encoding).decode("utf-8"))
            picture_src_list = data.xpath('//*[@id="ctid"]/@src')
            picture_title_list = data.xpath('/html/body/div[1]/h2/text()')
            pattern = re.compile(r"【(.+)】")
            result = pattern.findall(picture_title_list[0])
            print(picture_src_list, result)

            if picture_src_list and result:
                for picture_src in picture_src_list:
                    cur = self.db.cursor()
                    sql_insert = "insert into picture(create_time,title,img_url,status,number) values(%s,%s,%s,%s,%s)"
                    cur.execute(sql_insert, (int(time.time()), result[0], picture_src, 1, i))
                    # 提交
                    self.db.commit()
                    print("success=====================", result[0], picture_src)
        self.db.close()
        return self


a = LihHeSpider()
a.get_picture()
