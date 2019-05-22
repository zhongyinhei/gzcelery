# -*- coding:utf-8 -*-
import pickle
import random

from lxml import html

from database.redis_mangager import RedisDB
from database.sqllite_operate import YCTCATLOG, RETRUNOPTION, session
from handle_data import celery_app
from tool.utils import *

REDIS_GZ = RedisDB()


@celery_app.task(name='to_create')
def to_create(data):
    '''解析出所有的退回数据,将pickle的数据做解析'''
    if data:
        order_number = str(random.random())
        REDIS_GZ.set(order_number, data, ex=3600)
        to_analysis.apply_async(args=[order_number], retry=True, queue='to_analysis', immutable=True)
        # to_analysis(order_number)


@celery_app.task(name='to_analysis')
def to_analysis(order_number):
    '''解析出所有退回的信息'''
    data_bytes = REDIS_GZ.get(order_number)
    # data_str = data_bytes.decode(encoding='utf-8')
    data_str = pickle.loads(eval(data_bytes))
    response_text = data_str['response_text']()
    if 'http://yct.sh.gov.cn/portal_yct/webportal/handle_progress.do' in data_str['to_server']:
        result = REDIS_GZ.hget('specify_account_yctAppNo_page')
        if result['total']:
            if result['getpage'] == result['total']:
                return
        tree = html.fromstring(response_text)
        res = tree.xpath('string(//td[@class="text_grey"])')
        try:
            getpage, total = re.compile('\d+').findall(res)[:2]
        except ValueError as e:
            return
        REDIS_GZ.hset('specify_account_yctAppNo_page', {'getpage': getpage, 'total': total})
        infos = []
        try:
            for tr, trs in zip(tree.xpath('//div[@class="cc_text fR"]/ul'), tree.xpath('//div[@class="com_box"]')):
                info = {}
                name = clean(tr.xpath('string(self::*/../../../../h4)'))
                company_xpath = tr.xpath('self::*/../../../../div//span[@title="删除"]/@onclick')
                id_ = deal_kuohao(company_xpath).split(',')[-1]
                info['license'] = clean(tr.xpath('string(./li[@class="first_c"]/span)'))
                info['chapter'] = clean(tr.xpath('string((.//span)[2])'))
                info['matter'] = clean(tr.xpath('string((.//span)[3])'))
                info['bespoke'] = clean(tr.xpath('string((.//span)[4])'))
                info['company_name'] = name
                info['yctAppNo'] = id_
                # info['pagecode'] = html_text
                info['lincense_state'] = '0'
                infos.append(info)
        except Exception as e:
            print(e)

    elif 'http://yct.sh.gov.cn/bizhallnz_yctnew/apply/appendix/print' in data_str['to_server']:
        infos = {}
        yctAppNo = data_str['to_server'].split('yctAppNo=')[-1]
        tree = html.fromstring(response_text)
        text = tree.xpath('string(.//div[normalize-space(text())="预审结果：退回修改"]/../..)')
        data = pretrial_info(text)
        corporation_name = data['corporation_name']  # 公司的名称
        engage_range_repair = data['manage_scope']  # 经营范围修改
        other_content = data['other_repair']  # 其他内容
        infos['company_name'] = corporation_name
        infos['engage_range_repair'] = engage_range_repair
        infos['yctAppNo'] = yctAppNo
        infos['other_content'] = other_content
        infos['label'] = 'RETRUNOPTION'
    else:
        return
    to_save.apply_async(args=[infos], retry=True, queue='to_save', immutable=True)


@celery_app.task(name='to_save')
def to_save(res):
    if (type(res).__name__ == 'dict'):
        if res['label'] == 'RETRUNOPTION':
            try:
                inquery_result = session.query(RETRUNOPTION).filter_by(yctAppNo=res['yctAppNo']).first()
                if inquery_result.company_name != res['company_name'] or inquery_result.engage_range_repair != res[
                    'engage_range_repair'] or inquery_result.other_content != res['other_content']:
                    session.delete(inquery_result)
                    session.commit()
                    result = RETRUNOPTION(yctAppNo=res['yctAppNo'], other_content=res['other_content'],
                                          company_name=res['company_name'],
                                          engage_range_repair=res['engage_range_repair'])
                    session.add(result)
                    session.commit()
                    session.execute(
                        'update yctcatlog set lincense_state = 1 where yctAppNo = "{}"'.format(res['yctAppNo']))
            except AttributeError as e:
                result = RETRUNOPTION(yctAppNo=res['yctAppNo'], other_content=res['other_content'],
                                      company_name=res['company_name'],
                                      engage_range_repair=res['engage_range_repair'])
                session.add(result)
                session.commit()
            # print(res['yctAppNo'])
            REDIS_GZ.hdel('specify_account_yctAppNo', res['yctAppNo'])
    elif type(res).__name__ == 'list':
        for i in res:
            try:
                inquery_result = session.query(YCTCATLOG).filter_by(yctAppNo=i['yctAppNo']).first()
                license = inquery_result.license
                chapter = inquery_result.chapter
                matter = inquery_result.matter
                bespoke = inquery_result.bespoke
                if license == '退回修改':
                    REDIS_GZ.hset('specify_account_yctAppNo', {i['yctAppNo']: '退回修改'})
                if license != i['license'] or chapter != i['chapter'] or matter != i['matter'] or bespoke != i[
                    'bespoke']:
                    session.delete(inquery_result)
                    session.commit()
                else:
                    continue
            except AttributeError as e:
                pass
            result = YCTCATLOG(license=i['license'], chapter=i['chapter'], matter=i['matter'], bespoke=i['bespoke'],

                               company_name=i['company_name'], yctAppNo=i['yctAppNo'],
                               lincense_state=i['lincense_state'])
            session.add(result)
            session.commit()
        return
