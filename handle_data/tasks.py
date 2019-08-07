# -*- coding:utf-8 -*-
## 13585582354
## 147258369zaq

#9b4de30e40c5447ab0d09d4f569ba628
import pickle
import random
import urllib.parse as Parse

from lxml import html

from database.redis_mangager import RedisDB
from database.sqllite_operate import YCTCATLOG, RETRUNOPTION, SUCCESSFULCOMPLETION, session
from handle_data import celery_app
from tool.utils import *

REDIS_GZ = RedisDB()


# @celery_app.task(name='to_create')
def to_create(data):
    '''解析出所有的退回数据,将pickle的数据做解析'''
    if data:
        order_number = str(random.random())
        REDIS_GZ.set(order_number, data, ex=360)
        # to_analysis.apply_async(args=[order_number], retry=True, queue='to_analysis', immutable=True)
        # 避免错误赋值的问题
        to_analysis(order_number)


# @celery_app.task(name='to_analysis')
def to_analysis(order_number):
    '''解析出所有退回的信息'''
    data_bytes = REDIS_GZ.get(order_number)
    # data_str = data_bytes.decode(encoding='utf-8')
    data_str = pickle.loads(eval(data_bytes))
    response_text = data_str['response_text']()
    #print(data_str['to_server'])
    if '申请信息填写人需进行实名认证' in response_text or '服务器错误' in response_text:
        return
    # elif 'x=12' in data_str['to_server']:
    #     REDIS_GZ.hset('specify_account_yctAppNo_page', {'getpage': '-1', 'total': '-2'})
    #     return
    elif 'http://yct.sh.gov.cn/portal_yct/webportal/handle_progress.do' in data_str['to_server']:
        result = REDIS_GZ.hget('specify_account_yctAppNo_page')
        tree = html.fromstring(response_text)
        res = tree.xpath('string(//td[@class="text_grey"])')
        getpage, total = re.compile('\d+').findall(res)[:2]
        #print(getpage,'i am getpage')
        infos = []
        if int(getpage) > int(result['getpage']):
            REDIS_GZ.hset('specify_account_yctAppNo_page', {'getpage': getpage, 'total': total})
            try:
                for tr, trs in zip(tree.xpath('//div[@class="cc_text fR"]/ul'), tree.xpath('//div[@class="com_box"]')):
                    info = {}
                    name = clean(tr.xpath('string(self::*/../../../../h4)'))
                    company_xpath = tr.xpath('self::*/../../../../div//span[@title="删除"]/@onclick')
                    id_ = deal_kuohao(company_xpath).split(',')[-1]
                    info['license'] = clean(tr.xpath('string(./li[@class="first_c"]/span)'))
                    if '填报成功' in info['license']:
                        info['license'] = '填报成功（查看详情） （ 就业参保 企业选择不办理 ）'
                    info['chapter'] = clean(tr.xpath('string((.//span)[2])'))
                    info['matter'] = clean(tr.xpath('string((.//span)[3])'))
                    info['bespoke'] = clean(tr.xpath('string((.//span)[4])'))
                    info['company_name'] = name
                    info['yctAppNo'] = id_
                    html_text = html.tostring(trs, encoding='utf-8').decode()
                    info['pagecode_1'] = html_text[0:1000]
                    info['pagecode_2'] = html_text[1000:2000]
                    info['pagecode_3'] = html_text[2000:3000]
                    info['pagecode_4'] = html_text[3000:4000]
                    info['lincense_state'] = '0'
                    infos.append(info)
            except Exception as e:
                pass
                #print(e)

    elif 'http://yct.sh.gov.cn/bizhallnz_yctnew/apply/appendix/print' in data_str['to_server']:
        yctAppNo = data_str['to_server'].split('yctAppNo=')[-1]
        infos = {}
        if '填报成功' in response_text:
            tree = html.fromstring(response_text)
            for tr, trs in zip(tree.xpath("//input[@type='image']/@onclick"),
                               tree.xpath("//input[@type='image']/../../td[2]")):
                parms, stuff = tr, trs.xpath('string()')
                stuff = stuff.replace(' ', '')
                result = re.compile('\d+[A-Z]\d+|\d+').findall(parms)
                parms = '^'.join(result)
                infos[parms] = stuff
                for z in range(4):
                    try:
                        inquery_result = session.query(SUCCESSFULCOMPLETION).filter_by(yctAppNo=yctAppNo).first()
                        session.close()
                        if inquery_result:
                            break
                        else:
                            REDIS_GZ.hset('specify_account_tbcg_' + yctAppNo, infos)
                            break
                    except Exception as e:
                        session.rollback()
                        session.close()
                        if z == 3:
                            raise e
            return
        else:
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
    elif 'http://yct.sh.gov.cn/bizhallnz_yctnew/apply/appendix/content_special' in data_str[
        'to_server'] or 'http://yct.sh.gov.cn/bizhallnz_yctnew/apply/appendix/content' in data_str['to_server']:
        infos = {}
        yctAppNo = data_str['to_server'].split('yctAppNo=')[-1]
        infos['label'] = 'SUCCESSFULCOMPLETION'
        infos['content'] = response_text
        infos['yctAppNo'] = yctAppNo
        papers = Parse.unquote(data_str['to_server'].split('papers=')[1].split('&')[0])
        result = REDIS_GZ.hget('specify_account_tbcg_' + yctAppNo)
        infos['papers'] = result.get(papers, '')
        infos['papers_perm'] = papers
    else:
        return
    # to_save.apply_async(args=[infos], retry=True, queue='to_save', immutable=True)
    to_save(infos)


# @celery_app.task(name='to_save')
def to_save(res):
    if (type(res).__name__ == 'dict'):
        if res['label'] == 'RETRUNOPTION':
            try:
                inquery_result = session.query(RETRUNOPTION).filter_by(yctAppNo=res['yctAppNo']).first()
                if inquery_result.company_name != res['company_name'] or inquery_result.engage_range_repair != res[
                    'engage_range_repair'] or inquery_result.other_content != res['other_content']:
                    session.delete(inquery_result)
                    session.commit()
                    session.close()
                    result = RETRUNOPTION(yctAppNo=res['yctAppNo'], other_content=res['other_content'],
                                          company_name=res['company_name'],
                                          engage_range_repair=res['engage_range_repair'])
                    session.add(result)
                    session.commit()
                    session.close()
                    try:
                        session.execute(
                            'update yctcatlog set lincense_state = 1 where yctAppNo = "{}"'.format(res['yctAppNo']))
                    except Exception as e:
                        session.rollback()
                        raise e
            except AttributeError as e:
                result = RETRUNOPTION(yctAppNo=res['yctAppNo'], other_content=res['other_content'],
                                      company_name=res['company_name'],
                                      engage_range_repair=res['engage_range_repair'])
                session.add(result)
                session.commit()
                session.close()
            except Exception as e:
                session.rollback()
            REDIS_GZ.hdel('specify_account_yctAppNo', res['yctAppNo'])
        elif res['label'] == 'SUCCESSFULCOMPLETION':
            response_text = res['content']
            try:
                result = SUCCESSFULCOMPLETION(yctAppNo=res['yctAppNo'],
                                              papers=res['papers'],
                                              content_1=response_text[0:2000],
                                              content_2=response_text[2000:4000],
                                              content_3=response_text[4000:6000],
                                              content_4=response_text[6000:8000],
                                              content_5=response_text[8000:10000],
                                              content_6=response_text[10000:12000],
                                              content_7=response_text[12000:14000],
                                              content_8=response_text[14000:16000],
                                              content_9=response_text[18000:20000],
                                              content_10=response_text[20000:22000]
                                              )
                session.add(result)
                session.commit()
                session.close()
            except Exception as e:
                session.rollback()
            else:
                REDIS_GZ.hdel('specify_account_tbcg_' + res['yctAppNo'], res['papers_perm'])
                res_len = REDIS_GZ.hget('specify_account_tbcg_' + res['yctAppNo'])
                if not res_len:
                    REDIS_GZ.hdel('specify_account_yctAppNo', res['yctAppNo'])

    elif type(res).__name__ == 'list':
        for i in res:
            try:
                inquery_result = session.query(YCTCATLOG).filter_by(yctAppNo=i['yctAppNo']).first()
                if inquery_result:
                    license = inquery_result.license
                    chapter = inquery_result.chapter
                    matter = inquery_result.matter
                    bespoke = inquery_result.bespoke
                    if '退回修改' in license:
                        REDIS_GZ.hset('specify_account_yctAppNo', {i['yctAppNo']: '退回修改'})
                    if license != i['license'] or chapter != i['chapter'] or matter != i['matter'] or bespoke != i[
                        'bespoke']:
                        session.delete(inquery_result)
                        session.commit()
                        session.close()
                        if '退回修改' in license:
                            result = YCTCATLOG(license=i['license'], chapter=i['chapter'], matter=i['matter'],
                                               bespoke=i['bespoke'],
                                               company_name=i['company_name'], yctAppNo=i['yctAppNo'],
                                               lincense_state=i['lincense_state'],
                                               pagecode_1=i['pagecode_1'], pagecode_2=i['pagecode_2'],
                                               pagecode_3=i['pagecode_3'], pagecode_4=i['pagecode_4'])
                            session.add(result)
                            session.commit()
                            session.close()
                            continue
                        elif '填报成功' in license:
                            if license == i['license'] and chapter == i['chapter'] and matter == i[
                                'matter'] and bespoke == \
                                    i['bespoke']:
                                continue
                            else:
                                try:
                                    result = YCTCATLOG(license=i['license'], chapter=i['chapter'], matter=i['matter'],
                                                       bespoke=i['bespoke'],
                                                       company_name=i['company_name'], yctAppNo=i['yctAppNo'],
                                                       lincense_state=i['lincense_state'],
                                                       pagecode_1=i['pagecode_1'], pagecode_2=i['pagecode_2'],
                                                       pagecode_3=i['pagecode_3'], pagecode_4=i['pagecode_4'])
                                    session.add(result)
                                    session.commit()
                                    session.close()
                                except Exception as e:
                                    session.rollback()
                                continue
                    else:
                        continue
            except Exception as e:
                session.rollback()
            try:
                result = YCTCATLOG(license=i['license'], chapter=i['chapter'], matter=i['matter'], bespoke=i['bespoke'],

                                   company_name=i['company_name'], yctAppNo=i['yctAppNo'],
                                   lincense_state=i['lincense_state'],
                                   pagecode_1=i['pagecode_1'], pagecode_2=i['pagecode_2'],
                                   pagecode_3=i['pagecode_3'], pagecode_4=i['pagecode_4'])
                session.add(result)
                session.commit()
                session.close()
            except Exception as e:
                session.rollback()
            else:
                if '填报成功' in i['license']:
                    REDIS_GZ.hset('specify_account_yctAppNo', {i['yctAppNo']: '填报成功'})
                elif '退回修改' in i['license']:
                    REDIS_GZ.hset('specify_account_yctAppNo', {i['yctAppNo']: '退回修改'})
        return
