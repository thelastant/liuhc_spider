import re

import requests
import time
from lxml import etree
import pymysql

from celery_pro.utils.config import config


class ArticleSpider(object):
    def __init__(self):
        self.db = pymysql.connect(host=config.SPIDER_HOST, user=config.SPIDER_USER,
                                  password=config.SPIDER_PASSWORD, db=config.SPIDER_DB, port=config.SPIDER_PORT)

    def get_picture(self):
        for i in range(1, 20):
            main_url = "https://www.89829m.com/bbs/bbs"
            main_url += "0" + str(i) if i < 10 else str(i)
            main_url += ".html"
            response = requests.get(url=main_url, timeout=20)
            text = response.text
            # print(text.encode(response.encoding).decode("utf-8"))
            html = etree.HTML(text.encode(response.encoding).decode("utf-8"))
            li_list = html.xpath("/html/body/div[4]/div/ul/li")

            # 标题
            title = html.xpath("/html/body/div[4]/div/h3/text()")
            period = title[0][1:4]
            print(title, period)

            for li in li_list:
                text_list = li.xpath("./text()")  #
                text_2 = li.xpath("./span/text()")  # 猜测
                text_3 = li.xpath("./span/u/text()")[0] if li.xpath("./span/u/text()") else ""  # 中
                text_4 = li.xpath("./font/text()")[0] if li.xpath("./font/text()") else ""  # 结果
                print(text_list, text_2, text_3, text_4)
                kai_1 = text_2[1] if len(text_2) == 2 else ""
                kai_2 = text_2[0] if text_2 else ""
                guess = kai_2 + text_3 + kai_1
                result = text_4
                content_1 = text_list[0] if text_list else ""
                content_2 = text_list[1] if len(text_list) == 2 else ""
                content_3 = text_list[2] if len(text_list) == 3 else ""
                content = content_1 + guess + content_2 + result + content_3
                print(content)
                self.save_in_db(title=title, period=period, content=content, result=result, guess=guess)
        self.db.close()

        return self

    def save_in_db(self, title, period, content, result, guess):
        cur = self.db.cursor()
        sql_insert = "insert into article(create_time,title,period,content,result,guess) values(%s,%s,%s,%s,%s,%s)"
        cur.execute(sql_insert, (int(time.time()), title, period, content, result, guess))
        # 提交
        self.db.commit()
        return self


a = ArticleSpider().get_picture()
