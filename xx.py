# -*- coding:utf-8 -*-
with open(file='./xx.html',encoding='utf-8') as folder:
    x=folder.read()
# print(x)

a="""
<div class="com_box">
			<h4 class="com_tile">
				上海青浦明天石化助剂有限责任公司
			</h4>
			<div class="com_con">
				<span title="删除" class="com_icon_del" onclick="javascript:del('fb96a0ea761945e5b1bbcde8bf3e2dfc','0000000120181126A031','7010','905dedc6974a4ec5922b1c2aba537cb3');"></span>
			<span class="com_icon_bxs" title="设置不再显示" onclick="javascript:hideDel('fb96a0ea761945e5b1bbcde8bf3e2dfc','0000000120181126A031','7010');"></span>
				<div class="com_chart_tip">
					<ul>
						<li><i class="icon_green"></i>已完成</li>
						<li><i class="icon_red"></i>退回/不通过</li>
						<li><i class="icon_yellow"></i>正在进行</li>
						<li><i class="icon_blue"></i>未开始</li>
						<li><i class="icon_purple"></i>自助办理</li>
					</ul>
				</div>
				<div class="c_chart_c">
					<div class="cc_chart_2 fL">
				<a href="javascript:edit('7010','905dedc6974a4ec5922b1c2aba537cb3','10')" class="cc_a" id="notBlank1_0" style="cursor: pointer;">
				<span class="cc_piece">
				
					
						<i class="circle_yellow"></i>
						<script type="text/javascript">
						$("#notBlank1_0").attr("href","javascript:edit('7010','905dedc6974a4ec5922b1c2aba537cb3','10')");
						$("#notBlank1_0").css("cursor","pointer");
						</script>
					
					
				
					<em>一表填报</em>
				</span>
				</a>
				<a href="javascript:void(0);" style="cursor:default;" class="cc_b">
					<span class="cc_piece">
					
					
						<i class="circle_blue"></i>
					
					
					
					
					
					
					
						<em>业务办理</em>
					</span>
				</a>
				 <a href="javascript:void(0);" style="cursor:default;" class="cc_c">
					<span class="cc_piece">
					
						
							<i class="circle_blue"></i>
						
						
						
						
						
						
					
						<em>优化服务</em>
					</span>
				</a>
				<a href="javascript:void(0);" style="cursor:default;" class="cc_d" id="notBlank2_0">
					<span class="cc_piece">
						
						
							<i class="circle_blue"></i>
						
						
						
						
						
						
					
						<em>营业执照办理</em>
					</span>
				</a>
				<a href="javascript:void(0);" style="cursor:default;" class="cc_e">
					<span class="cc_piece">
					
						
						
							<i class="circle_blue"></i>
						
						
						
						
						
						
					
						<em style="padding-left: 13px;padding-right: 13px;">公章刻制</em>
					</span>
				</a>
				<a href="javascript:void(0);" style="cursor:default;" class="cc_f">
					<span class="cc_piece">
					
						
						
							<i class="circle_blue"></i>
						
						
						
						
						
						
					
						<em>涉税事项</em>
					</span>
				</a>
				<a href="javascript:void(0);" style="cursor:default;" class="cc_g">
					<span class="cc_piece">
					
						
						
							<i class="circle_blue"></i>
						
						
						
						
						
						
					
						<em>银行预约开户</em>
					</span>
				</a>
				<a href="javascript:void(0);" style="cursor:default;" class="cc_h">
					<span class="cc_piece">
						<i class="circle_purple"></i>
						<em>社保用工自助办理</em>
					</span>
				</a>
				</div>
					<div class="cc_text fR">
						<ul>
							<li class="first_c">
								<i></i>
								<span>
									
										
										
										
										
											<a href="javascript:edit('7010','905dedc6974a4ec5922b1c2aba537cb3','10')" style="cursor: pointer;">一表填报信息已确认</a>
										
									
								</span>
							<!-- 	营业执照预审退回，请按照退回意见的要求修改填报内容 -->
							</li>
							<li>
								<i></i>
								<span>
								
									
									
									
									
										
										 <!-- 公安一窗领取特殊处理 -->
											
												
												
													一表填报信息待确认
												
											
										
										
									
									
									
								
								</span>
							<!-- 	公章刻制备案信息审核中 -->
							</li>
							<li>
								<i></i>
								<span>
								
									
									
									
										一表填报信息待确认
									
								
								</span>
							<!-- 	涉税事项信息审核中 -->
							</li>
							<li>
								<i></i>
								<span>
								
									
									
									一表填报信息待确认
									
								
								</span>
							<!-- 	银行开户信息审核中 -->
							
							</li>
							<li>
								<i></i>
								<span>
									
										
										
										
										
										
										
											待填报
										
									
								</span>
<!-- 								<span>请登录<a href="https://zzjb.12333sh.gov.cn/zzjbdl/jsp/login.jsp" style="cursor:pointer;color:blue;" target="_blank">自助经办系统</a>自助办理 -->
<!-- 								</span> -->
							<!-- 	社保用工自助办理未开始 -->
							</li>
						</ul>
					</div>
				</div>
			 </div>
		 </div>
"""
from lxml import html
z=html.fromstring(x)
for i in z.xpath('//div[@class="com_box"]'):
    x=html.tostring(i,encoding='utf-8').decode()
    print(len(x))
    aa=x[0:1000]
    bb=x[1000:2000]
    cc=x[2000:3000]
    dd=x[3000:4000]
    ee=x[4000:5000]
