import requests
from lxml import etree
from queue import Queue
import pymysql
from celery_pro.utils.image_storage import run_save_img
from celery_pro.utils.config import config
from datetime import datetime
from celery_pro.utils.common import img_src_cai_tu, img_src_cai_tu_source
from celery_pro.utils.image_storage import save_img_and_get_info


class GetPictureData(object):
    def __init__(self, first=1, second=1, third=1):
        self.first = first  # 1：第一个网站开启
        self.second = second  # 1：第二个网站开启
        self.third = third  # 1:第一网站公式图片开启
        self.q = Queue()
        self.xpath_pattern_1 = "//tr/td/p/img/@src"  # 第一网站获取图片链接
        self.xpath_pattern_2 = "//div[5]/div/h2/font/text()"  # 第一网站获取图片标题
        self.index_url = "http://908181.com/caitu/"  # 第一网站基础url
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

        self.index_url_3 = "http://908181.com/gs/888.html"  # 第一网站公式图片基础url
        self.xpath_pattern_9 = "//tr/td/a/@href"  # 第一网站公式图片获取url规则
        self.xpath_pattern_10 = "//div[5]/div/h2"  # 第一网站公式图片标题 h2标签
        self.xpath_pattern_11 = "//tr/td//tr/td/img/@src"  # 第一网站公式图片标题 src链接

    def get_response(self, url, response_type=1):
        if response_type == 1:
            response = requests.get(url=url, timeout=15)
            response = response.text.encode(response.encoding).decode("utf-8")
            html = etree.HTML(response)
        elif response_type == 2:
            response = requests.get(url=url,timeout=15)
            html = response.content
        else:
            response = requests.get(url=url,timeout=15)
            response = response.text
            html = etree.HTML(response)
        return html

    def deal_data(self, html, xpath_pattern):
        data = html.xpath(xpath_pattern)
        return data

    def check_is_save(self, type_num, source, img_src):
        db = pymysql.connect(host=config.SPIDER_HOST, user=config.SPIDER_USER,
                             password=config.SPIDER_PASSWORD, db=config.SPIDER_DB, port=config.SPIDER_PORT)
        cur = db.cursor()
        sql_insert = "SELECT * FROM picture WHERE type=%s AND source=%s AND img_src=%s"

        try:
            res = cur.execute(sql_insert, (type_num, source, img_src))
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
        # create_time = time.time()
        source = kwargs.get("source_url")
        source_type = kwargs.get("type_num")
        status = 1
        # true_src = kwargs.get("true_src", None)
        # 2.插入操作
        db = pymysql.connect(host=config.SPIDER_HOST, user=config.SPIDER_USER,
                             password=config.SPIDER_PASSWORD, db=config.SPIDER_DB, port=config.SPIDER_PORT)

        cur = db.cursor()
        sql_insert = "insert into picture(create_time,img_title,img_src,source,status,type) values(%s,%s,%s,%s,%s,%s)"
        try:
            cur.execute(sql_insert, (create_time, img_title, img_src, source, status, source_type))
            # 提交
            db.commit()
            print(img_title, img_src, create_time, source, "存入数据库成功!!!!!!!!!")
        except Exception as e:
            # 错误回滚
            print("保存图片失败", e)
            db.rollback()
        finally:
            db.close()

    def update_picture(self, **kwargs):
        img_src = kwargs.get("img_src", None)
        update_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        source = kwargs.get("source_url")
        source_type = kwargs.get("type_num")
        img_high = kwargs.get("img_high")
        img_width = kwargs.get("img_width")

        # 2.插入操作
        db = pymysql.connect(host=config.SPIDER_HOST, user=config.SPIDER_USER,
                             password=config.SPIDER_PASSWORD, db=config.SPIDER_DB, port=config.SPIDER_PORT)

        cur = db.cursor()
        sql_insert = "UPDATE picture SET update_time=%s,img_src=%s,img_high=%s,img_width=%s WHERE source=%s AND type=%s"
        # sql_insert = "UPDATE USER SET PASSWORD='"+pwd+"' WHERE NAME='"+name+"'"

        try:
            cur.execute(sql_insert, (update_time, img_src, img_high, img_width, source, source_type))
            # 提交
            db.commit()
            print(img_src, update_time, source, "更新数据库成功!!!!!!!!!")
        except Exception as e:
            # 错误回滚
            print("更新图片失败", e)
            db.rollback()
        finally:
            db.close()

    def save_in_qiniu(self, type_num, img_content, img_title, img_src, url):
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
        data["true_src"] = true_img_url
        data["source_url"] = url
        data["source_type"] = 1
        if 96 >= type_num > 56:
            data["source_type"] = 2
        elif type_num > 96:
            data["source_type"] = 3
        else:
            pass
        print("存入七牛成功！！！！！")
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

    def run_picture_1(self, save_method=1):
        """  第一个网站  """

        total_picture = 56
        for type_num in range(1, total_picture + 1):
            data = {}
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
            data["source_url"] = url

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
            # 获取图片数据src
            try:
                if type_num == 15 or type_num == 16:
                    img_src = "http://908181.com/" + img_src
            except:
                print(type_num, img_title, "=======下载失败")
                continue
            img_content = self.get_response(url=img_src, response_type=2)
            img_info = save_img_and_get_info(img_num=type_num, img_data=img_content)
            data["img_high"] = img_info["high"]
            data["img_width"] = img_info["high"]
            data["type_num"] = type_num
            data["source_url"] = url
            data["img_src"] = img_src
            data["img_title"] = img_title
            if save_method == 1:
                self.save_to_db(**data)
            elif save_method == 2:
                self.update_picture(**data)
            else:
                print(type_num, "图片存入数据库失败")
                continue
            print("==============", type_num, img_src)

    def run_picture_2(self):
        """  第二个网站  """
        img_response = self.get_response(url=self.index_url_2)
        img_url_list = self.deal_data(html=img_response, xpath_pattern=self.xpath_pattern_8)
        type_num = 56
        for img in img_url_list:
            type_num += 1
            img_url = "http://9542.34266.com/9542zl/" + img.xpath("@href")[0]  # 图片url
            img_title = img.xpath("text()")[0]  # 图片标题
            img_res = self.get_response(url=img_url, response_type=3)  # 请求图片url返回体
            img_src = self.deal_data(html=img_res, xpath_pattern=self.xpath_pattern_5)[0]  # 图片src
            img_content = self.get_response(url=img_src, response_type=2)  # 请求src返回体，图片数据

            # 检查图片是否已经存入数据库
            is_save = self.check_is_save(type_num=type_num, source=img_url, img_src=img_src)
            if is_save:
                print("=================img has been save", img_title, img_src)
                continue
            # 图片存入七牛云
            data = self.save_in_qiniu(type_num=type_num, img_content=img_content, img_title=img_title, img_src=img_src,
                                      url=img_url)
            # 图片存入数据库
            self.save_to_db(**data)

    def run_picture_3(self, save_method=1):
        """  第一个网站公式图片  """
        data = {}
        try:
            img_response = self.get_response(url=self.index_url_3)
        except:
            img_response = self.get_response(url=self.index_url_3)
        img_url_list = self.deal_data(html=img_response, xpath_pattern=self.xpath_pattern_9)
        type_num = 56
        for img in img_url_list:
            type_num += 1
            img_url = "http://908181.com/gs/" + img  # 图片url

            try:
                img_data = self.get_response(url=img_url, response_type=1)  # 图片页面所有内容（包含文字）
            except:
                try:
                    img_data = self.get_response(url=img_url, response_type=1)  # 图片页面所有内容（包含文字）
                except:
                    img_data = self.get_response(url=img_url, response_type=1)  # 图片页面所有内容（包含文字）

            img_deal_data = self.deal_data(html=img_data, xpath_pattern=self.xpath_pattern_10)[0]
            img_title_1 = img_deal_data.xpath("text()")[0]
            img_title_3 = img_deal_data.xpath("text()")[1]
            img_title_2 = img_deal_data.xpath("//font/text()")[0]
            img_title = img_title_1 + img_title_2 + img_title_3
            img_src = self.deal_data(html=img_data, xpath_pattern=self.xpath_pattern_11)[0]

            # 拼接src
            if len(img_src) < 15:
                img_src = "http://908181.com" + img_src[1:2]
            else:
                img_src = img_src
            try:
                img_content = self.get_response(url=img_src, response_type=2)
                img_info = save_img_and_get_info(img_num=type_num, img_data=img_content)
            except:
                img_info = {"img_high": 0, "img_width": 0}
            data["img_high"] = img_info["high"]
            data["img_width"] = img_info["high"]
            data["type_num"] = type_num
            data["source_url"] = img_url
            data["img_src"] = img_src
            data["img_title"] = img_title
            if save_method == 1:
                self.save_to_db(**data)
            elif save_method == 2:
                self.update_picture(**data)
            else:
                continue
            print("==============", type_num, img_src)

    def run_one_picture(self, url, type_num, xpath_pattern_1):
        data = {}
        try:
            html = self.get_response(url=url)
            img_src = self.deal_data(html=html, xpath_pattern=xpath_pattern_1)[0]  # 图片链接
        except:
            return False
        if not img_src:
            print("==图片下载失败==url==%s" % url)
            return False
        # 获取图片数据src
        try:
            if type_num == 15 or type_num == 16:
                img_src = "http://908181.com/" + img_src
        except:
            print(type_num, img_src, "=======下载失败")
            return False

        if type_num > 56:
            img_src = "http://www.908282.com" + img_src[2:]

        try:
            img_content = self.get_response(url=img_src, response_type=2)
            img_info = save_img_and_get_info(img_num=type_num, img_data=img_content)
        except:
            img_info = {"img_high": 0, "img_width": 0}

        # 更新数据库
        data["type_num"] = type_num
        data["img_src"] = img_src
        data["source_url"] = url
        data["img_high"] = img_info["high"]
        data["img_width"] = img_info["high"]
        self.update_picture(**data)
        return True

    def run(self):

        # 908181网站分类图片
        for i in range(1, 81):
            # 根据不一样的内容先确定不同的爬取规则
            if i <= 56:
                xpath_pattern_img = self.xpath_pattern_1
            else:
                xpath_pattern_img = self.xpath_pattern_11
            try:
                result = self.run_one_picture(url=img_src_cai_tu_source[i], type_num=i,
                                              xpath_pattern_1=xpath_pattern_img)
            except:
                try:
                    result = self.run_one_picture(url=img_src_cai_tu_source[i], type_num=i,
                                                  xpath_pattern_1=xpath_pattern_img)
                except:
                    continue
            if not result:
                print("图片更新失败,将会重新爬取整个网站！")
                self.run_picture_1(save_method=2)
                self.run_picture_3(save_method=2)
                print("所有数据更新成功！")
                break
        print("所有图片检查完成")


# # 测试！！！！！！！！！！
obj = GetPictureData()
obj.run()
