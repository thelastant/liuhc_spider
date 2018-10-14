import requests
from lxml import etree
from queue import Queue
import pymysql
from celery_pro.utils.config import config
from datetime import datetime
from celery_pro.utils.common import article_url
from celery_pro.utils import article_deal_func


class GetArticleData(object):
    def __init__(self, first=1, second=1):
        self.first = first  # 1：第一个网站开启
        self.second = second  # 1：第二个网站开启
        self.q = Queue()
        self.base_url = "http://www.908282.com"

        # 有规律的帖子
        self.index_url_10 = "http://www.908282.com/bbs/999.html"  # 这个精华帖子主页url
        self.xpath_pattern_5 = "//td/a"  # 精华帖子a标签筛选规则
        self.xpath_pattern_6 = "//tr/td/font/text()"  # 帖子内容筛选规则

        # 没有规律的帖子
        self.index_url = "http://www.908282.com/bbs/888.html"  # 第一网站基础url
        self.xpath_pattern_1 = "//tr[4]/td/a/text()[1]"  # 获取期数的筛选规则
        self.xpath_pattern_2 = "//tr/td/font/span"  # 获取第一篇文章筛选规则

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

    def check_is_save(self, periods=None, result=None, title=None, title_id=None):
        db = pymysql.connect(host=config.SPIDER_HOST, user=config.SPIDER_USER,
                             password=config.SPIDER_PASSWORD, db=config.SPIDER_DB, port=config.SPIDER_PORT)
        cur = db.cursor()
        sql_insert = "SELECT * FROM article WHERE periods=%s AND title=%s AND result=%s"
        sql_insert_2 = "SELECT * FROM article_title WHERE title=%s AND rid=%s"
        if title_id:
            try:
                res = cur.execute(sql_insert_2, (title, title_id))
            except Exception as e:
                print(e, "title db ======")
                return False
            db.close()
        else:
            try:
                res = cur.execute(sql_insert, (periods, title, result))
            except Exception as e:
                print(e, "result db======")
                return False
            db.close()
        if res:
            return True
        else:
            return False

    def save_to_db(self, **kwargs):

        title_2 = kwargs.get("title_2", None)
        title_id = kwargs.get("title_id", None)
        periods = kwargs.get("periods", None)
        create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        source = kwargs.get("source_url")
        guess_all = kwargs.get("guess_all", None)
        status = 1
        guess_true = kwargs.get("guess_right", None)
        result = kwargs.get("result", None)

        # 检查是否重复存储
        try:
            is_save = self.check_is_save(periods=periods, result=result, title=title_2)
        except:
            is_save = None

        if is_save:
            print("数据已存在，请勿重复存储")
            return

        # 2.插入操作
        db = pymysql.connect(host=config.SPIDER_HOST, user=config.SPIDER_USER,
                             password=config.SPIDER_PASSWORD, db=config.SPIDER_DB, port=config.SPIDER_PORT)
        cur = db.cursor()
        sql_insert_1 = "insert into article(create_time,title,periods,source_url,status,guess_all,guess_true,result,title_id) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        try:
            cur.execute(sql_insert_1,
                        (create_time, title_2, periods, source, status, guess_all, guess_true, result, title_id))
            db.commit()
            # 提交
        except Exception as e:
            # 错误回滚
            print("保存图片失败", e)
            db.rollback()
        finally:
            db.close()

    def save_to_db_2(self, **kwargs):
        """   存入文章标题   """
        title = kwargs.get("title", None)
        title_id = kwargs.get("title_id", None)
        create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        status = 1

        # 检查是否重复存储数据库
        try:
            is_save = self.check_is_save(title_id=title_id, title=title)
        except:
            is_save = None
        if is_save:
            print("请勿重复存储")
            return

        # 2.插入操作
        db = pymysql.connect(host=config.SPIDER_HOST, user=config.SPIDER_USER,
                             password=config.SPIDER_PASSWORD, db=config.SPIDER_DB, port=config.SPIDER_PORT)
        cur = db.cursor()
        sql_insert_2 = "insert into article_title(rid,title,status,create_time) values(%s,%s,%s,%s)"
        try:
            cur.execute(sql_insert_2, (title_id, title, status, create_time))
            db.commit()
            # 提交
        except Exception as e:
            # 错误回滚
            print("保存数据库失败", e)
            db.rollback()
        finally:
            db.close()

    def run_article_1(self):
        """  908282网站文章  """
        # 第一层获取文章链接
        response = self.get_response(url=self.index_url_10)
        data_list = self.deal_data(html=response, xpath_pattern=self.xpath_pattern_5)
        num = 0
        for data in data_list:
            num += 1
            if num == 6 or num == 10:
                continue
            href = data.xpath("@href")[0]
            href = "http://www.908282.com" + href[2:]  # 拼接成完整url
            title_1 = data.xpath("text()")[0]
            title_2 = data.xpath("font/text()")[0]
            title = title_1 + title_2
            periods = int(title_1[1:4])
            title_id = int(str(periods) + str(num))

            print(href, title_1, title_2, periods, title_id)
            self.deal_article_data_1(href=href, title=title, periods=periods, title_id=title_id, title_2=title_2)

    def func_select(self, d, i=1):
        if i == 1:
            result = article_deal_func.func_1(d)
        else:
            result = ''
        return result

    def run_article_new(self):

        # 获取期数
        try:
            html = self.get_response(url=self.index_url)
        except:
            print("爬取失败")
            return
        periods = self.deal_data(html=html, xpath_pattern=self.xpath_pattern_1)[0][1:4]
        if periods:
            periods = int(periods)
        num = 8
        for i in range(1, 13):
            num += 1
            print(i)
            if i not in [1]:
                break
            response = self.get_response(url=article_url[i])

            # 初步筛选规则的选择
            xpath_pattern = article_deal_func.select_xpath_pattern(i=i)

            # 初步筛选数据
            data = self.deal_data(html=response, xpath_pattern=xpath_pattern)
            title_0 = self.deal_data(html=response, xpath_pattern="//div/h2/font/text()")[0]

            article_title_dict = {}
            article_title_dict["title"] = "第" + str(periods) + "期" + ":" + "精华帖" + " " + title_0
            article_title_dict["title_id"] = str(periods) + str(num)

            # 保存标题到数据库
            self.save_to_db_2(**article_title_dict)

            for d in data:
                # 筛选文章内容的函数
                result = self.func_select(d=d, i=i)

                # 保存结果到数据库
                self.deal_article_data_2(href=article_url[i], title=title_0,
                                         periods=periods,
                                         title_id=article_title_dict["title_id"], result=result)
                print(result, periods, title_0)

    def deal_article_data_1(self, href, title, periods, title_id, title_2):
        response = self.get_response(url=href, response_type=1)
        data_list = self.deal_data(html=response, xpath_pattern=self.xpath_pattern_6)
        # 一篇文章存一次标题
        title_dict = {}
        title_dict["title"] = title
        title_dict["title_id"] = title_id
        self.save_to_db_2(**title_dict)

        for data in data_list:
            data_list = {}
            data_list["source_url"] = href
            data_list["title"] = title
            data_list["periods"] = periods
            data_list["result"] = data.strip()
            data_list["title_id"] = title_id
            data_list["title_2"] = title_2
            print("===>", data_list)
            self.save_to_db(**data_list)

    def deal_article_data_2(self, href, title, periods, title_id, result):
        # 一篇文章存一次标题
        data_list = {}
        data_list["source_url"] = href
        data_list["periods"] = periods
        data_list["result"] = result
        data_list["title_id"] = title_id
        data_list["title_2"] = title
        print("===>", result)
        self.save_to_db(**data_list)

    def run(self):
        self.run_article_1()
        self.run_article_new()


obj = GetArticleData()
obj.run()
