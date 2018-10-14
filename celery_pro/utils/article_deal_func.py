xpath_pattern_1 = '//tr/td/font/span'  # 1200
xpath_pattern_2 = '//tr/td/font'  # 1202


def select_xpath_pattern(i):
    if i == 1:
        xpath_pattern = xpath_pattern_1
    elif i == 2:
        xpath_pattern = xpath_pattern_2
    else:
        xpath_pattern = ''
    return xpath_pattern


def func_1(d):
    result_1 = d.xpath("font[1]/text()")[0]  # 期数标题
    result_2 = d.xpath("font[2]/text()")[0]  # 预测内容1
    if len(result_2) > 14:
        result_2 = " 【预测数据暂未公布1】"
    try:
        result_3 = d.xpath("font[2]/text()")[1]  # 预测内容
    except:
        result_3 = ''
    try:
        result_4 = d.xpath("font[2]/span/text()")[0]
    except:
        result_4 = ''
    try:
        result_5 = d.xpath("font[3]/text()")[0]
    except:
        result_5 = ''
    result = result_1 + result_2 + result_4 + result_3 + result_5
    return result


def fun_2(d):
    try:
        result_1 = d.xpath("//div/h2/font/text()")[0]  # 期数
    except:
        result_1 = ''
    try:
        result_2 = d.xpath("//tr/td/font/font/text()")[0]  # 标题？？结果里面的标题
    except:
        result_2 = ""
    try:
        result_3 = d.xpath("//tr/td/font/font/text()")[1]  # 预测
    except:
        result_3 = ''
    try:
        result_4 = d.xpath("//tr/td/font/font/text()")[2]  # 开奖结果
    except:
        result_4 = ''
    try:
        result_5 = d.xpath("//div/h2/font/text()")[1]  # ->开
    except:
        result_5 = ''
    try:
        result_6 = d.xpath("//div/h2/font/text()")[2]  # 准？
    except:
        result_6 = ''

    result = result_1 + result_2 + result_3 + result_5 + result_4 + result_6
    return result