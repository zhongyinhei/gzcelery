from database.redis_mangager import RedisDB
REDIS_GZ = RedisDB()
import re
res='234'
getpage, total = re.compile('\d+').findall(res)[:2]
REDIS_GZ.hset('specify_account_yctAppNo', {'32345454321': '退回修改'})
# data_str={}
# data_str['to_server']='http://yct.sh.gov.cn/bizhallnz_yctnew/apply/appendix/content?id=-7964922&appendixStatus=&isPrint=1&p=1&yctAppNo=faee7e7331ea42f58400c72a1e441209'
# import urllib.parse as Parse
# papers = Parse.unquote(data_str['to_server'].split('papers=')[1].split('&')[0])
# print(papers)
# from database.sqllite_operate import YCTCATLOG, RETRUNOPTION, SUCCESSFULCOMPLETION, session
# inquery_result = session.query(YCTCATLOG).filter_by(yctAppNo=i['yctAppNo']).first()
# if inquery_result:
# specify_account_yctAppNo = REDIS_GZ.hget('specify_account_yctAppN')
# print(specify_ac、count_yctAppNo)
# result=REDIS_GZ.hget('specify_account_tbcg_'+'faee7e7331ea42f58400c72a1e441209')
# print(result)
# REDIS_GZ.hset('specify_account_session', {'session': 'true'})
# specify_account_yctAppNo = REDIS_GZ.hget('specify_account_session')
# print(specify_account_yctAppNo)
# REDIS_GZ.hset('specify_account_session', {'session': 'false'})
# specify_account_yctAppNo = REDIS_GZ.hget('specify_account_session')
# print(specify_account_yctAppNo)
# print(specify_account_yctAppNo)
# from tool.utils import pretrial_info
# from lxml import html
# with open(file='./bb.html',encoding='utf-8') as folder:
#     response_text=folder.read()
#
# tree = html.fromstring(response_text)
# text = tree.xpath('string(.//div[normalize-space(text())="预审结果：退回修改"]/../..)')
# data = pretrial_info(text)
# print(data)
#
# corporation_name = data['corporation_name']  # 公司的名称
# engage_range_repair = data['manage_scope']  # 经营范围修改
# other_content = data['other_repair']
# print(corporation_name,engage_range_repair,other_content)
# REDIS_GZ = RedisDB()
# x=REDIS_GZ.hget('specify_account_tbcg_faee7e7331ea42f58400c72a1e441209')
# a='8003844'
# y=x[a]
# print(y)
# # REDIS_GZ.hset('specify_account_yctAppNo_page', {'getpage': 0, 'total': ''})
# from lxml import html
# import re
# from database.redis_mangager import RedisDB

# with open(file='./zz.html',encoding='utf-8') as folder:
#     text=folder.read()
# tree=html.fromstring(text)
# yctAppNo='faee7e7331ea42f58400c72a1e441209'
# infos={}
# for tr ,trs in zip(tree.xpath("//input[@type='image']/@onclick"),tree.xpath("//input[@type='image']/../../td[2]")) :
#     a,b=tr,trs.xpath('string()')
#     b=b.replace(' ','')
#     x=re.compile('\d+[A-Z]\d+|\d+').findall(a)
#     parm='&'.join(x)
#     infos[parm]=b
# print(infos)

# REDIS_GZ.hset('specify_account_tbcg_'+yctAppNo, infos)
#
# from database.sqllite_operate import YCTCATLOG, RETRUNOPTION, SUCCESSFULCOMPLETION,session
# yctAppNo='be187e4ed8214959abcee0f659885b4f'
# with open(file='./lingqu.html',encoding='utf-8') as folder:
#     content=folder.read()
# papers='全体合伙人签署的委托执行事务合伙人的委托书；执行事务合伙人是法人或其他组织的，还应当提交其委派代表的委托书和身份证明复印件'
# print(len(content))
# content_1=content[0:2000]
# content_2=content[2000:4000]
# content_3=content[4000:6000]
# content_4=content[6000:8000]
# content_5=content[8000:10000]
# content_6=content[10000:12000]
# content_7=content[12000:14000]
# content_8=content[14000:16000]
# content_9=content[18000:20000]
# content_10=content[20000:22000]
# result = SUCCESSFULCOMPLETION(yctAppNo=yctAppNo,
# papers=papers,content_1=content_1,content_2=content_2,content_3=content_3,content_4=content_4,
#                               content_5=content_5,content_6=content_6,content_7=content_7,
#                               content_8=content_8,content_9=content_9,content_10=content_10)
#
# session.add(result)
# session.commit()
# session.close()
#
#
#
#
# import urllib.parse as p
# x='http://yct.sh.gov.cn/bizhallnz_yctnew/apply/appendix/content?id=-7964971&appendixStatus=&isPrint=1&p=1&papers=%E5%85%A8%E4%BD%93%E5%90%88%E4%BC%99%E4%BA%BA%E7%AD%BE%E7%BD%B2%E7%9A%84%E5%A7%94%E6%89%98%E6%89%A7%E8%A1%8C%E4%BA%8B%E5%8A%A1%E5%90%88%E4%BC%99%E4%BA%BA%E7%9A%84%E5%A7%94%E6%89%98%E4%B9%A6%EF%BC%9B%E6%89%A7%E8%A1%8C%E4%BA%8B%E5%8A%A1%E5%90%88%E4%BC%99%E4%BA%BA%E6%98%AF%E6%B3%95%E4%BA%BA%E6%88%96%E5%85%B6%E4%BB%96%E7%BB%84%E7%BB%87%E7%9A%84%EF%BC%8C%E8%BF%98%E5%BA%94%E5%BD%93%E6%8F%90%E4%BA%A4%E5%85%B6%E5%A7%94%E6%B4%BE%E4%BB%A3%E8%A1%A8%E7%9A%84%E5%A7%94%E6%89%98%E4%B9%A6%E5%92%8C%E8%BA%AB%E4%BB%BD%E8%AF%81%E6%98%8E%E5%A4%8D%E5%8D%B0%E4%BB%B6&yctAppNo=23lk4j23klaslkdfj'
# if 'papers' in x:
#     p=x.split('yctAppNo=')[-1]
#     print(p)
    # y=x.split('papers=')[1].split('&')
    # v=y[0]
    # z=y[1].split('yctAppNo=')[-1]
    # print(z)
    # url = p.unquote(v)
    # print(url)

# from database.sqllite_operate import YCTCATLOG, RETRUNOPTION, SUCCESSFULCOMPLETION, session
# inquery_result = session.query(SUCCESSFULCOMPLETION).filter_by(yctAppNo='be187e4ed8214959abcee0f659885b4f').first()
# print(inquery_result)


# from lxml import html
# from tool.utils import *
# with open(file='./hh.html',encoding='utf-8') as folder:
#     text=folder.read()
# tree=html.fromstring(text)
# for tr, trs in zip(tree.xpath('//div[@class="cc_text fR"]/ul'), tree.xpath('//div[@class="com_box"]')):
#     info = {}
#     name = clean(tr.xpath('string(self::*/../../../../h4)'))
#     company_xpath = tr.xpath('self::*/../../../../div//span[@title="删除"]/@onclick')
#     id_ = deal_kuohao(company_xpath).split(',')[-1]
#     info['license'] = clean(tr.xpath('string(./li[@class="first_c"]/span)'))
#     print(info)
#     print(id_)
#     print(name)