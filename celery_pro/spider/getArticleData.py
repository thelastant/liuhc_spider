import requests
from lxml import etree
from queue import Queue
import pymysql
from celery_pro.utils.image_storage import run_save_img
from celery_pro.utils.config import config
from datetime import datetime


class GetArticleData(object):
    def __init__(self, first=1, second=1):
        self.first = first  # 1：第一个网站开启
        self.second = second  # 1：第二个网站开启
        self.q = Queue()

        self.index_url = "http://www.908282.com/bbs/888.html"  # 第一网站基础url
        self.xpath_pattern_1 = "/html/body/table/tbody/tr/td/a"  # 第一网站获取文章规则（a标签）

        self.xpath_pattern_2 = "//div[5]/div/h2/font/text()"  # 第一网站获取图片标题
        self.index_url_2 = "http://9542.34266.com/9542zl/tg.htm"  # 第二网站基础url
        self.last_url = "http://908181.com/caitu/%E7%BA%A2%E8%B4%A2%E7%A5%9E.gif"
        self.xpath_pattern_3 = "//tr[2]/td/a/span/font/text()"  # 第一网站筛选期数规则

        self.xpath_pattern_4 = "//tr[1]/td[1]/font/span/a/font/text()"  # 第二网站的期数筛选规则
        self.get_periods_url_1 = "http://www.908282.com/908181.html"  # 第一网站筛选期数 url
        self.get_periods_url_2 = "http://9542.34266.com/9542zl/888.htm"  # 第二期数筛选期数url

        self.xpath_pattern_5 = "//p[2]/img/@src"  # 第二网站图片链接筛选规则 src
        self.xpath_pattern_6 = "//div/dl/dd/a/text()"  # 第二网站图片标题筛选规则
        self.xpath_pattern_7 = "//div/dl/dd/a/@href"  # 第二网站图片..筛选规则
        self.xpath_pattern_8 = "//div/dl/dd/a"  # 第二网站图片..筛选规则

    def get_response(self, url, response_type=1):
        if response_type == 1:
            response = requests.get(url=url)
            response = response.text.encode(response.encoding).decode("utf-8")
            html = etree.HTML(response)
        elif response_type == 2:
            response = requests.get(url=url)
            html = response.content
        else:
            response = requests.get(url=url)
            response = response.text
            html = etree.HTML(response)
        return html

    def deal_data(self, html, xpath_pattern):
        data = html.xpath(xpath_pattern)
        return data

    def check_is_save(self, periods, source, img_src):
        db = pymysql.connect(host=config.SPIDER_HOST, user=config.SPIDER_USER,
                             password=config.SPIDER_PASSWORD, db=config.SPIDER_DB, port=config.SPIDER_PORT)
        cur = db.cursor()
        sql_insert = "SELECT * FROM picture WHERE periods=%s AND source=%s AND img_src=%s"

        try:
            res = cur.execute(sql_insert, (periods, source, img_src))
        except Exception as e:
            print(e)
            return False
        db.close()
        if res:
            return True
        else:
            return False

    def save_to_db(self, **kwargs):
        img_title = kwargs.get("img_title", None)
        img_src = kwargs.get("img_src", None)
        create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        source = kwargs.get("source_url")
        source_type = kwargs.get("source_type")
        status = 1
        periods = kwargs.get("periods", None)
        true_src = kwargs.get("true_src", None)
        print(img_title, img_src, create_time, source, periods, true_src, "!!!!!!!!!")
        # 2.插入操作
        db = pymysql.connect(host=config.SPIDER_HOST, user=config.SPIDER_USER,
                             password=config.SPIDER_PASSWORD, db=config.SPIDER_DB, port=config.SPIDER_PORT)

        cur = db.cursor()
        sql_insert = "insert into picture(create_time,img_title,img_src,source,status,periods,true_src,type) values(%s,%s,%s,%s,%s,%s,%s,%s)"
        try:
            cur.execute(sql_insert, (create_time, img_title, img_src, source, status, periods, true_src, source_type))
            # 提交
            db.commit()
        except Exception as e:
            # 错误回滚
            print("保存图片失败", e)
            db.rollback()
        finally:
            db.close()

    def save_in_qiniu(self, type_num, img_content, img_title, img_src, periods):
        data = {}
        try:
            true_img_url = run_save_img(img_num=type_num, img_data=img_content)
        except Exception as e:
            true_img_url = run_save_img(img_num=type_num, img_data=img_content)

        if true_img_url:
            true_img_url = "http://p3o5hwuoa.bkt.clouddn.com/" + true_img_url
        # 存入数据库
        data["img_title"] = img_title
        data["img_src"] = img_src
        data["periods"] = periods
        data["true_src"] = true_img_url
        data["source_url"] = self.index_url
        data["source_type"] = 1
        if type_num > 56:
            data["source_url"] = self.index_url_2
            data["source_type"] = 2
        return data

    def check_new_periods(self, source_type):

        if source_type == 1:
            source_url = self.get_periods_url_1
            xpath_pattern = self.xpath_pattern_3
            # source = self.index_url
            response_type = 1
        elif source_type == 2:
            source_url = self.get_periods_url_2
            xpath_pattern = self.xpath_pattern_4
            # source = self.index_url_2
            response_type = 3

        else:
            return False
        res = self.get_response(url=source_url, response_type=response_type)
        periods = self.deal_data(html=res, xpath_pattern=xpath_pattern)[0][:3]
        print(periods)
        periods = int(periods)
        # 检查数据是否最新
        # if self.check_is_save(periods=periods, source=source):
        #     print("已经是最新的一期了")

        #     return False
        return periods

    def run_article_1(self):
        """  第一个网站  """

        periods = self.check_new_periods(source_type=1)
        if not periods:
            return False
        article_response = self.get_response(url=self.index_url, response_type=3)
        article_data_list = self.deal_data(html=article_response, xpath_pattern=self.xpath_pattern_1)
        for article_data in article_data_list:
            article_title = article_data.xpath("text()")

        for type_num in range(1, total_picture + 1):
            # 第一个网站拼接url
            if len(str(type_num)) == 1:
                type_string = "0" + "0" + str(type_num)
            elif len(str(type_num)) == 2:
                type_string = "0" + str(type_num)
            else:
                type_string = str(type_num)
            url = self.index_url
            url += type_string
            url += ".html"
            img_pattern = self.xpath_pattern_1
            title_pattern = self.xpath_pattern_2
            try:
                html = self.get_response(url=url)
                img_src = self.deal_data(html=html, xpath_pattern=img_pattern)[0]  # 图片链接
                img_title = self.deal_data(html=html, xpath_pattern=title_pattern)[0]  # 图片标题
            except:
                self.q.put(url)
                continue
            if not all([img_src, img_title]):
                print("==%s图片下载失败==url==%s" % (img_title, url))
                continue
            print("==============", type_num, img_src)
            # 获取图片数据src
            try:
                if type_num == 15 or type_num == 16:
                    img_src = "http://908181.com/" + img_src
                img_content = self.get_response(url=img_src, response_type=2)
            except:
                print(type_num, img_title, "=======下载失败")
                continue

            # 检查数据库是否已经保存图片
            is_save = self.check_is_save(periods=periods, source=self.index_url, img_src=img_src)
            if is_save:
                print("=================img has been save", periods, img_title, img_src)
                continue

            # 存入七牛，返回字典
            data = self.save_in_qiniu(type_num=type_num, img_content=img_content, img_title=img_title,
                                      img_src=img_src, periods=periods)
            # 存入数据库
            self.save_to_db(**data)
            # # 下载失败后在队列中取出来，重新请求下载
            # while not self.q.empty():
            #     a = self.q.get()
            #     print(a, "qqqqqqq")

    def run_picture_2(self):
        """  第二个网站  """
        periods = self.check_new_periods(source_type=2)
        if not periods:
            return False
        img_response = self.get_response(url=self.index_url_2)
        img_url_list = self.deal_data(html=img_response, xpath_pattern=self.xpath_pattern_8)
        type_num = 57
        for img in img_url_list:
            img_url = "http://9542.34266.com/9542zl/" + img.xpath("@href")[0]  # 图片url
            img_title = img.xpath("text()")[0]  # 图片标题
            img_res = self.get_response(url=img_url, response_type=3)  # 请求图片url返回体
            img_src = self.deal_data(html=img_res, xpath_pattern=self.xpath_pattern_5)[0]  # 图片src
            img_content = self.get_response(url=img_src, response_type=2)  # 请求src返回体，图片数据

            # 检查图片是否已经存入数据库
            is_save = self.check_is_save(periods=periods, source=self.index_url_2, img_src=img_src)
            if is_save:
                print("=================img has been save", periods, img_title, img_src)
                continue
            # 图片存入七牛云
            data = self.save_in_qiniu(type_num=type_num, img_content=img_content, img_title=img_title, img_src=img_src,
                                      periods=periods)
            # 图片存入数据库
            self.save_to_db(**data)
            type_num += 1

    def run(self):
        if self.first in [1, "1"]:
            self.run_picture_1()
        if self.second in [1, "1"]:
            self.run_picture_2()
        return True

# # 测试！！！！！！！！！！
# obj = GetPictureData()
# obj.run()
