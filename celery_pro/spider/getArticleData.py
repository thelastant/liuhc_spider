import requests
from lxml import etree
from queue import Queue
import pymysql
from celery_pro.utils.config import config
from datetime import datetime


class GetArticleData(object):
    def __init__(self, first=1, second=1):
        self.first = first  # 1：第一个网站开启
        self.second = second  # 1：第二个网站开启
        self.q = Queue()
        self.base_url = "http://www.908282.com"

        self.index_url = "http://www.908282.com/bbs/888.html"  # 第一网站基础url
        self.xpath_pattern_1 = "//tr/td/a"  # 获取文章规则（a标签）
        self.xpath_pattern_2 = "//tr/td/p/font/b"  # 获取文章内容规则1
        self.xpath_pattern_3 = "//tr/td/font"  # 获取文章标题2
        self.xpath_pattern_4 = "//tr/td/font/font"  # 获取网站2 预测内容规则

        self.index_url_8 = "http://www.908282.com/bbs/pt.html"  # 这个是平特一肖的开奖url
        self.index_url_9 = "http://www.908282.com/bbs/1166.html"  # 这个是规律六肖的开奖url
        self.index_url_10 = "http://www.908282.com/bbs/999.html"  # 这个精华帖子主页url
        self.xpath_pattern_5 = "//td/a"  # 精华帖子a标签筛选规则
        self.xpath_pattern_6 = "//tr/td/font/text()"  # 帖子内容筛选规则

        # self.index_url_2 = "http://9542.34266.com/9542zl/tg.htm"  # 第二网站基础url
        # self.last_url = "http://908181.com/caitu/%E7%BA%A2%E8%B4%A2%E7%A5%9E.gif"
        # self.xpath_pattern_4 = "//tr[1]/td[1]/font/span/a/font/text()"  # 第二网站的期数筛选规则
        # self.get_periods_url_1 = "http://www.908282.com/908181.html"  # 第一网站筛选期数 url
        # self.get_periods_url_2 = "http://9542.34266.com/9542zl/888.htm"  # 第二期数筛选期数url
        #
        # self.xpath_pattern_5 = "//p[2]/img/@src"  # 第二网站图片链接筛选规则 src
        # self.xpath_pattern_6 = "//div/dl/dd/a/text()"  # 第二网站图片标题筛选规则
        # self.xpath_pattern_7 = "//div/dl/dd/a/@href"  # 第二网站图片..筛选规则
        # self.xpath_pattern_8 = "//div/dl/dd/a"  # 第二网站图片..筛选规则

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
        periods = int(periods)
        return periods

    def save_to_db_2(self, **kwargs):
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
            periods = int(periods)
            return periods

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

    def deal_article_data_1(self, href, title, periods, title_id, title_2):

        response = self.get_response(url=href, response_type=1)
        data_list = self.deal_data(html=response, xpath_pattern=self.xpath_pattern_6)
        num = 0
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
            print(num, "===>", data_list)

            self.save_to_db(**data_list)


            # if len(href[0]) <= 17:
            #     href = "http://www.908282.com" + href[2:]
            # print(href, title, "=========>success")
            #
            # try:
            #     article_response = self.get_response(url=href)
            # except:
            #     print(href, title, "=========>fail")
            #     return
            # if self.deal_data(html=article_response, xpath_pattern=self.xpath_pattern_2):
            #     article_list = self.deal_data(html=article_response, xpath_pattern=self.xpath_pattern_2)
            # elif self.deal_data(html=article_response, xpath_pattern=self.xpath_pattern_3):
            #     article_list = self.deal_data(html=article_response, xpath_pattern=self.xpath_pattern_3)
            # else:
            #     return
            # for a in article_list:
            #     data = {}
            #     data["title"] = title
            #     data["href"] = href
            #     try:
            #         text_1 = a.xpath("text()")[0].strip()
            #         text_true = a.xpath("text()")[1].strip()
            #         text_right_1 = a.xpath("span/font/text()")
            #         text_guess = a.xpath("font/text()")
            #         text_right_2 = a.xpath("font/span/text()")
            #         data["periods"] = int(text_1[:3])
            #     except:
            #         text_1 = ""
            #         text_true = ""
            #         text_guess = []
            #         text_right_1 = ""
            #         text_right_2 = ""
            #
            #     if text_1 or text_true:
            #         # 数据清洗，筛选出预测生肖
            #         if text_guess:
            #             text_guess_new = []
            #             guess_result = ''
            #             for res_1 in text_guess:
            #                 if res_1 != "（":
            #                     try:
            #                         list_b = res_1.split(",")
            #                     except:
            #                         list_b = []
            #                     for res_2 in list_b:
            #                         if res_2 == '':
            #                             continue
            #                         try:
            #                             f = res_2.split("）")
            #                             for res_3 in f:
            #                                 if res_3 != '':
            #                                     try:
            #                                         res = res_3.split("（")
            #                                         for r in res:
            #                                             if r != '':
            #                                                 guess_result += ',%s' % r
            #                                                 text_guess_new.append(r)
            #                                     except:
            #                                         continue
            #                         except:
            #                             pass
            #         if text_right_1:
            #             guess_result = guess_result + "," + text_right_1[0]
            #             data["guess_right"] = text_right_1
            #             print(text_1, text_right_1[0], text_guess_new, text_true, title, href, guess_result, "if===")
            #         elif text_right_2:
            #             guess_result = guess_result + "," + text_right_2[0]
            #             data["guess_right"] = text_right_2
            #             print(text_1, text_right_2[0], text_guess_new, text_true, title, href, guess_result, "elif==")
            #         else:
            #             if num == 2:  # 第二篇文章中最新一期预测筛选规则不一样
            #                 guess_result = text_guess_new[0]
            #             else:
            #                 print(text_guess_new)
            #                 guess_result = text_guess_new[0] + "," + text_guess_new[1] + "," + text_guess_new[2] + "," + \
            #                                text_guess_new[3]
            #             print(text_1, text_right_2, type(text_right_2), text_guess_new, text_true, href, "else==")
            #         data["guess_all"] = guess_result
            #         data["result"] = text_true
            #         self.save_to_db(**data)
            #         print(data, "data=============data")
            #     else:
            #         continue

    def run(self):
        self.run_article_1()


obj = GetArticleData()
obj.run_article_1()
