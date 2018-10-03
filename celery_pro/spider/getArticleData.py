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
        self.xpath_pattern_1 = "//tr/td/a"  # 获取文章规则（a标签）
        self.xpath_pattern_2 = "//tr/td/p/font/b"  # 获取文章内容规则1
        self.xpath_pattern_3 = "//tr/td/font"  # 获取文章标题2

        self.index_url_2 = "http://9542.34266.com/9542zl/tg.htm"  # 第二网站基础url
        self.last_url = "http://908181.com/caitu/%E7%BA%A2%E8%B4%A2%E7%A5%9E.gif"
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
        """  908282网站文章  """
        # 第一层获取文章链接
        response = self.get_response(url=self.index_url)
        data_list = self.deal_data(html=response, xpath_pattern=self.xpath_pattern_1)
        for data in data_list:
            href = data.xpath("@href")[0]
            title = data.xpath("text()")
            if len(href[0]) <= 17:
                href = "http://www.908282.com" + href[2:]
            print(href, title, "=========>success")

            try:
                article_response = self.get_response(url=href)
            except:
                print(href, title, "=========>fail")

                continue
            if self.deal_data(html=article_response, xpath_pattern=self.xpath_pattern_2):
                article_list = self.deal_data(html=article_response, xpath_pattern=self.xpath_pattern_2)
            elif self.deal_data(html=article_response, xpath_pattern=self.xpath_pattern_3):
                article_list = self.deal_data(html=article_response, xpath_pattern=self.xpath_pattern_3)
            else:
                continue
            for data in article_list:
                text = data.xpath("text()")[0].strip()
                if text:
                    print(text)
                else:
                    continue

    def run(self):
        self.run_article_1()


obj = GetArticleData()
obj.run_article_1()
