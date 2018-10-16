xpath_pattern_1 = '//tr/td/font/span'  # 1200
xpath_pattern_2 = '//tr/td/font'  # 1202
xpath_pattern_3 = '//tr/td/font'  # 1203
xpath_pattern_4 = '//tr/td/font'  # 1204
xpath_pattern_5 = '//tr/td/p/font/b'  # 1205
xpath_pattern_6 = '//tr/td/font'  # 1208        需要加上介绍
xpath_pattern_7 = '//tr/td/span/font'  # 1209
xpath_pattern_8 = '//div[5]/table[2]//tr/td/table[1]//tr/td/p/font'  # 1210     需要加上介绍


def select_xpath_pattern(i):
    if i == 1:
        xpath_pattern = xpath_pattern_1
    elif i == 2:
        xpath_pattern = xpath_pattern_2
    elif i == 3:
        xpath_pattern = xpath_pattern_3
    elif i == 4:
        xpath_pattern = xpath_pattern_4
    elif i == 5:
        xpath_pattern = xpath_pattern_5
    elif i == 6:
        xpath_pattern = xpath_pattern_6
    elif i == 7:
        xpath_pattern = xpath_pattern_7
    elif i == 8:
        xpath_pattern = xpath_pattern_8
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
        print(result_5, "===>r5")
    except:
        result_5 = ''

    try:
        result_6 = d.xpath("font[4]/text()")[0]
    except:
        result_6 = ''
    try:
        result_7 = d.xpath("font[5]/text()")[0]
    except:
        result_7 = ''

    result = result_1 + result_2 + result_4 + result_3 + result_5 + result_6 + result_7
    return result


def fun_2(d):
    try:
        result_1 = d.xpath("text()")[0].strip()  # 期数
    except:
        result_1 = ''
    try:
        result_2 = d.xpath("font[1]/text()")[0].strip()  # 标题？？结果里面的标题
    except:
        result_2 = ""
    try:
        result_3 = d.xpath("font[2]/text()")[0].strip()  # 预测
    except:
        result_3 = ''
    try:
        result_4 = d.xpath("text()")[1].strip()  # —》开
    except:
        result_4 = ''
    try:
        result_5 = d.xpath("font[3]/text()")[0].strip()  # 开奖结果
    except:
        result_5 = ''
    try:
        result_6 = d.xpath("text()")[2].strip()  # 准？
    except:
        result_6 = ''

    result = result_1 + result_2 + result_3 + result_4 + result_5 + result_6
    return result.strip()


def fun_3(d):
    try:
        result_1 = d.xpath("text()")[0].strip()  # 期数
    except:
        result_1 = ''
    try:
        result_2 = d.xpath("font[1]/text()")[0].strip()  # 标题？？结果里面的标题1
    except:
        result_2 = ""
    try:
        result_3 = d.xpath("font[2]/text()")[0].strip()  # 标题？？结果里面的标题2
    except:
        result_3 = ''
    try:
        result_4 = d.xpath("font[3]/text()")[0].strip()  # 标题？？结果里面的标题3
    except:
        result_4 = ''
    try:
        result_5 = d.xpath("font[4]/text()")[0].strip()  # 标题？？结果里面的标题4
    except:
        result_5 = ''
    try:
        result_6 = d.xpath("font[5]/text()")[0].strip()  # 预测1 【
    except:
        result_6 = ''
    try:
        result_7 = d.xpath("span/font/text()")[0].strip()  # 预测2 单双（暂时只有一条结果有）
    except:
        result_7 = ''
    try:
        result_7_1 = d.xpath("font/span/text()")[0].strip()  # 预测2 单双（暂时只有一条结果有）
    except:
        result_7_1 = ''

    try:
        result_8 = d.xpath("font[6]/text()")[0].strip()  # 预测3 兔猪
    except:
        result_8 = ''
    try:
        result_9 = d.xpath("text()")[1].strip()  # ->开：
    except:
        result_9 = ''
    try:
        result_10 = d.xpath("font[7]/text()")[0].strip()  # 开奖结果 马41
    except:
        result_10 = ''
    try:
        result_11 = d.xpath("text()")[2].strip()  # 准！
    except:
        result_11 = ''
    try:
        result_12 = d.xpath("font[8]/text()")[0].strip()  # 开奖结果 马41
    except:
        result_12 = ''

    result = result_1 + result_2 + result_3 + result_4 + result_5 + result_6 + result_7 + result_7_1 + result_8 + result_9 + result_10 + result_11
    if result_7_1:
        result = result_1 + result_2 + result_3 + result_4 + result_5 + result_6 + result_7_1 + result_10 + result_9 + result_12 + result_11
    return result.strip()


def fun_4(d):
    try:
        result_1 = d.xpath("text()")[0].strip()  # 期数 + 标题名字
    except:
        result_1 = ''
    try:
        result_2 = d.xpath("font[1]/text()")[0].strip()  # 预测1，
    except:
        result_2 = ""
    try:
        result_3 = d.xpath("font[1]/span/text()")[0].strip()  # 预测11
    except:
        result_3 = ''
    try:
        result_4 = d.xpath("font[1]/text()")[1].strip()  # 预测2
    except:
        result_4 = ''
    try:
        result_5 = d.xpath("text()")[1].strip()  # ->开
    except:
        result_5 = ''
    try:
        result_6 = d.xpath("font[2]/text()")[0].strip()  # 开奖结果
    except:
        result_6 = ''
    try:
        result_7 = d.xpath("text()")[2].strip()  # 准！
    except:
        result_7 = ''
    result = result_1 + result_2 + result_3 + result_4 + result_5 + result_6 + result_7
    return result.strip()


def fun_5(d):
    try:
        result_1 = d.xpath("text()")[0].strip()  # 期数
    except:
        result_1 = ''
    try:
        result_2 = d.xpath("span/text()")[0].strip()  # 标题，
    except:
        result_2 = ""
    try:
        result_3 = d.xpath("font[1]/text()")[0].strip()  # 预测1
    except:
        result_3 = ''
    try:
        result_4 = d.xpath("span/font/text()")[0].strip()  # 预测2
    except:
        result_4 = ''
    try:
        result_5 = d.xpath("font[2]/text()")[0].strip()  # 预测3
    except:
        result_5 = ''
    try:
        result_6 = d.xpath("text()")[1].strip()  # ->开
    except:
        result_6 = ''
    try:
        result_7 = d.xpath("font[3]/text()")[0].strip()  # 结果
    except:
        result_7 = ''
    try:
        result_8 = d.xpath("text()")[2].strip()  # 准！
    except:
        result_8 = ''

    result = result_1 + result_2 + result_3 + result_4 + result_5 + result_6 + result_7 + result_8
    return result.strip()


def fun_6(d):
    try:
        result_1 = d.xpath("text()")[0].strip()  # 期数
    except:
        result_1 = ''
    try:
        result_2 = d.xpath("font[1]/text()")[0].strip()  # 标题，
    except:
        result_2 = ""
    try:
        result_3 = d.xpath("text()")[1].strip()  # ->->
    except:
        result_3 = ''
    try:
        result_4 = d.xpath("font[2]/text()")[0].strip()  # 预测1
    except:
        result_4 = ''
    try:
        result_5 = d.xpath("font[2]/span/text()")[0].strip()  # 预测2
    except:
        result_5 = ''
    try:
        result_6 = d.xpath("font[2]/text()")[1].strip()  #
    except:
        result_6 = ''
    try:
        result_7 = d.xpath("text()")[2].strip()  # 特码->开
    except:
        result_7 = ''
    try:
        result_8 = d.xpath("font[3]/text()")[0].strip()  # 结果
    except:
        result_8 = ''
    try:
        result_9 = d.xpath("text()")[3].strip()  # 准
    except:
        result_9 = ''
    result = result_1 + result_2 + result_3 + result_4 + result_5 + result_6 + result_7 + result_8 + result_9
    return result.strip()


def fun_7(d):
    try:
        result_1 = d.xpath("text()")[0].strip()  # 期数
    except:
        result_1 = ''
    try:
        result_2 = d.xpath("font[1]/text()")[0].strip()  # 预测1
    except:
        result_2 = ""
    try:
        result_3 = d.xpath("text()")[1].strip()  # 标题
    except:
        result_3 = ''
    try:
        result_4 = d.xpath("font[2]/text()")[0].strip()  # 预测2
    except:
        result_4 = ''
    try:
        result_5 = d.xpath("text()")[2].strip()  # 开
    except:
        result_5 = ''
    try:
        result_6 = d.xpath("font[3]/text()")[0].strip()  # 结果
    except:
        result_6 = ''
    try:
        result_7 = d.xpath("text()")[3].strip()  # 准
    except:
        result_7 = ''
    result = result_1 + result_2 + result_3 + result_4 + result_5 + result_6 + result_7
    print(result, "=====>>>>>>>result")

    return result.strip()


def fun_8(d):
    try:
        result_1 = d.xpath("text()")[0].strip()  # 期数
    except:
        result_1 = ''
    try:
        result_2 = d.xpath("span/text()")[0].strip()  # 标题
    except:
        result_2 = ""
    try:
        result_3 = d.xpath("span/font[1]/text()")[0].strip()  # 预测1
    except:
        result_3 = ''
    try:
        result_4 = d.xpath("span/font[1]/span/text()")[0].strip()  # 预测2
    except:
        result_4 = ''
    try:
        result_5 = d.xpath("span/font[1]/text()")[1].strip()  # )
    except:
        result_5 = ''
    try:
        result_6 = d.xpath("span/text()")[1].strip()  # 开
    except:
        result_6 = ''
    try:
        result_7 = d.xpath("span/font[2]/text()")[0].strip()  # 准
    except:
        result_7 = ''

    try:
        result_8 = d.xpath("span/text()")[2].strip()  # 准
    except:
        result_8 = ''
    result = result_1 + result_2 + result_3 + result_4 + result_5 + result_6 + result_7 + result_8
    print(result, "=====>>>>>>>result")

    return result.strip()
