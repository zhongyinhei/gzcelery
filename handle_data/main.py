# -*- coding:utf-8 -*-
from handle_data.tasks import *
# print('hello')
def handle_data(data_str):
    # res = chain(to_product.s(data_str), to_analysis.s(), to_consume.s())()

    # 插入一条pickle后的数据，返回记录的id res1
    res = to_create.apply_async(args=[data_str], retry=True, queue='to_create', immutable=True)
    # res = to_create(data_str)
    # print(res)