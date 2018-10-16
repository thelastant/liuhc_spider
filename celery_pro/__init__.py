# import random
#
# def test_the_win():
#     total = 100000                              # 总金额
#     b = 0                                       # 计算赢的次数
#     deposit = 10                                # 下注金额（第一次为10）
#     for i in range(0, 1000):                     # 总共下注次数
#         if total <= 0 or total < deposit:       # 开局总金额少于0  或者少于下注所需金额则终止循坏。
#             break
#         total -= deposit                         # 先给下注得钱 可以写成 total = total - deposit
#         if random.randint(0, 1) == 0:            # 如果0也就是出的是小，就是输了，
#
#             # 判断是否超过了需求的下注金额，最多翻倍9次
#             if deposit > 10*pow(2, 9):      # 10*2^9
#                 print(deposit, 10*pow(2, 9))
#                 deposit = 10  # 初始化下注金额
#                 continue
#
#             deposit = deposit*2                   # 输了就把下次的下注金额翻倍。然后结束这一轮
#             continue                            # 如果走到continue就结束本轮，后面的不执行了
#         b += 1                                   # 如果不走continue，则说明出的结果是1 就是大，赢了，先累计一次胜场
#         total += deposit*2                       # 赢了自然要把总金额加一下， 这里是本金+赢的，所以乘2
#         deposit = 10                             # 赢了之后按需求是要重置下注金额，从10 开始下注
#     print(total, b)                             # 最后打印出总金额，还有赢的次数
# # 运行函数
# test_the_win()

i = 0
while i < 5:
    i += 1
    if i == 3:
        break
    print(i)
