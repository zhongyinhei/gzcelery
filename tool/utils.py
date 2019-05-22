# -*- coding: utf-8 -*-
import re


# from downloader import Ftech
#
# FETCH = Ftech()
# PATH_WKH = r'I:\wkhtmltopdf\bin\wkhtmltopdf.exe'
# TTF_PATH = r'C:\Windows\Fonts\arial.ttf'


# def jpg(img):
#     '''处理jpg'''
#     im = open(img, 'rb').read()
#     return urlretrive(im)


def total_page(text):
    '''处理总页数'''
    return re.compile('\d+').findall(text)[0]


def deal_kuohao(text):
    '''处理括号'''
    if text:
        text = text[0]
        text = re.compile('\(.*?\)').findall(text)[0].replace('(', '').replace(')', '').replace("'", '')
        return text


def clean(text):
    '''清洗文本'''
    text = text.replace('\n', '').replace('\r', '').replace('\t', '')
    text = text.replace('\xa0', ' ')
    text = text.replace('\u3000\u3000\u3000', '　')
    return text


# def urlretrive(im):
#     '''下载图片'''
#     data = ''
#     try:
#         data = FETCH.rk_create(im=im, im_type=3000)['data']['result']
#     except Exception as e:
#         print(e)
#     finally:
#         return data


def injure_list(text):
    res = re.compile("[a-zA-Z0-9]{6,20}", re.S).findall(text)[1:]
    return res


def pretrial_info(text):
    '''获取预审信息'''
    try:
        x, y = text.replace(' ', '').replace('\n', '').split('企业名称')[-1].split('经营范围表述修改')
        z, p = y.split('其他内容修改')
        m = p.split('关闭')[0]
        x = x.replace('\r', '').replace('\t','')
        z = z.replace('\r', '').replace('\t','')
        m = m.replace('\r', '').replace('\t','')
    except Exception as e:
        print(text)
        import os
        os._exit(0)
    else:
        pretrial = {}
        pretrial['corporation_name'] = x
        pretrial['manage_scope'] = z
        pretrial['other_repair'] = m
        # ress = re.compile(r'<.*?/{0,1}>|\t|\n', re.I).sub('', text)
        # company = re.compile('企业名称[^经营范围表述修改]+|经营范围表述修改[^其他内容修改]+|其他内容修改[^关闭]+').findall(text)
        return pretrial


def html_deal(text, info):
    data = {}
    data['name'] = info
    data['file'] = text.encode('gbk', 'ignore').decode('gbk')
    return data
