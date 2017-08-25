# *-* coding: utf-8 *-*

from django.shortcuts import render, render_to_response
from django.http import HttpResponse, StreamingHttpResponse
from django.template import RequestContext
from django import forms
from django.utils import timezone
import simplejson
from datetime import *
import datetime as mydate
import time
import string
import xlrd
import os
import random
import qrcode

import sms
from .models import User, Phone, Timing, Shop, Goods, Discount, Friend, Advertisement, Prize, Order, OrderGoods
	

#from django.views.decorators.csrf import csrf_exempt
#@csrf_exempt
#base_url = 'http://127.0.0.1:8080/'
#base_url = 'http://qjzhzw.tunnel.qydev.com/'
#base_url = 'http://ab284a5f.ngrok.io/'
base_url = 'http://101.132.41.114:8080/'
MARK_PERCENT = 1 / float(60)#计时→积分兑换比率
TIME_MAX = 550 * 60#每日单人模式计时上限
VERSION_LATEST = float(1.0)#最新版本
IMAGE_DEFAULT = 'static/head/DEFUALT.png'#当图片不存在时，默认返回图片
PRIZE_PERCENT = 10#积分→抽奖次数兑换比率

def login(request):
#	if request.method == 'GET':
#		data_identification = '15061882150'
#		data_password = 'qiujiazuo'
	if request.method == 'POST':
		data_identification = request.POST['identification']#获取用户名
		data_password = request.POST['password']#获取密码
		
		result = User.objects.filter(identification = data_identification)#注意这里得到的是QuerySet类型
		
		data = {}
		if len(result) == 0:
			data['code'] = '201'
			data['msg'] = '该用户名不存在'
		elif cmp(result.last().password, data_password) != 0:
			data['code'] = '202'
			data['msg'] = '密码输入错误'
		else:
			result = result.last()
			#更新最后登录时间
			result.time_login = timezone.now()
			result.save()
			
			content = {}
			content['identification'] = result.identification
			content['nickname'] = string.strip(result.nickname)
			content['sex'] = result.sex
			content['birthday'] = str(result.birthday)
			content['motto'] = string.strip(result.motto)
			content['time'] = second_transfer(result.timing_useful)
			try:
				content['head'] = base_url + result.head.url
			except Exception, e:
				content['head'] = base_url + IMAGE_DEFAULT
				
			data['content'] = content
			data['code'] = '200'
			data['msg'] = '登录成功'
		
		return HttpResponse(simplejson.dumps(data))
		
		
def forget_vertification(request):
#	if request.method == 'GET':
#		data_identification = '15150147508'
	if request.method == 'POST':
		data_identification = request.POST['identification']#获取用户名
		
		result = User.objects.filter(identification = data_identification)#注意这里得到的是QuerySet类型
		
		data = {}
		if len(result) == 0:
			data['code'] = '201'
			data['msg'] = '该用户名不存在'
		else:
			get_code = sms.send(data_identification)#发送验证码
			
			phone = Phone()#创建手机号信息
			phone.identification = data_identification
			phone.code = get_code
			phone.code_start = time.strftime('%H:%M:%S',time.localtime(time.time()))#记录当前时间
			phone.save()
			
			data['code'] = '200'
			data['msg'] = '短信发送成功'
		
		return HttpResponse(simplejson.dumps(data))
		
		
def forget_login(request):
#	if request.method == 'GET':
#		data_identification = '15061882150'#获取用户名
#		data_code = '750649'#获取验证码
	if request.method == 'POST':
		data_identification = request.POST['identification']#获取用户名
		data_code = request.POST['code']#获取验证码
		
		result_phone = Phone.objects.filter(identification = data_identification)#注意这里得到的是QuerySet类型
		result_user = User.objects.filter(identification = data_identification)#注意这里得到的是QuerySet类型
		
		#记录当前时间
		try:
			result = result_phone.last()
			result.code_end = time.strftime('%H:%M:%S',time.localtime(time.time()))#记录当前时间
			result.save()
#			print result.code_start
#			print result.code_end
#			print sub_time(result_phone.last().code_start, result_phone.last().code_end)
		except Exception, e:
			print e
		
		data = {}
		if len(result_phone) == 0:
			data['code'] = '201'
			data['msg'] = '尚未发送验证码'
		elif cmp(result_phone.last().code, data_code) != 0:
			data['code'] = '202'
			data['msg'] = '验证码输入错误'
		elif sub_time(result_phone.last().code_start, result_phone.last().code_end) > 600:#定时600秒
			data['code'] = '203'
			data['msg'] = '验证码超时'
		elif len(result_user) == 0:
			data['code'] = '204'
			data['msg'] = '该用户名不存在'
		else:
			result = result_user.last()
			#更新最后登录时间
			result.time_login = timezone.now()
			result.save()
			
			content = {}
			content['identification'] = result.identification
			content['nickname'] = string.strip(result.nickname)
			content['sex'] = result.sex
			content['birthday'] = str(result.birthday)
			content['motto'] = string.strip(result.motto)
			content['time'] = second_transfer(result.timing_useful)
			try:
				content['head'] = base_url + result.head.url
			except Exception, e:
				content['head'] = base_url + IMAGE_DEFAULT
			
			data['content'] = content
			data['code'] = '200'
			data['msg'] = '登陆成功'
		
		return HttpResponse(simplejson.dumps(data))
		
		
def vertification(request):
#	if request.method == 'GET':
#		data_identification = '15150141111'
	if request.method == 'POST':
		data_identification = request.POST['identification']#获取用户名
		
		result = User.objects.filter(identification = data_identification)#注意这里得到的是QuerySet类型
		
		data = {}
		if len(result) != 0:
			data['code'] = '201'
			data['msg'] = '该手机号已被注册'
		else:
			get_code = sms.send(data_identification)#发送验证码
			
			phone = Phone()#创建手机号信息
			phone.identification = data_identification
			phone.code = get_code
			phone.code_start = time.strftime('%H:%M:%S',time.localtime(time.time()))#记录当前时间
			phone.save()
			
			data['code'] = '200'
			data['msg'] = '短信发送成功'
		
		return HttpResponse(simplejson.dumps(data))
		
		
def register(request):
#	if request.method == 'GET':
#		data_identification = '15150147508'#获取用户名
#		data_password = 'qjzhzw'#获取密码
#		data_code = '739184'#获取验证码
	if request.method == 'POST':
		data_identification = request.POST['identification']#获取用户名
		data_password = request.POST['password']#获取密码
		data_code = request.POST['code']#获取验证码
		
		result_phone = Phone.objects.filter(identification = data_identification)#注意这里得到的是QuerySet类型
		result_user = User.objects.filter(identification = data_identification)#注意这里得到的是QuerySet类型
		
		#记录当前时间
		try:
			result = result_phone.last()
			result.code_end = time.strftime('%H:%M:%S',time.localtime(time.time()))#记录当前时间
			result.save()
#			print result.code_start
#			print result.code_end
#			print sub_time(result_phone.last().code_start, result_phone.last().code_end)
		except Exception, e:
			print e
		
		data = {}
		if len(result_phone) == 0:
			data['code'] = '201'
			data['msg'] = '尚未发送验证码'
		elif cmp(result_phone.last().code, data_code) != 0:
			data['code'] = '202'
			data['msg'] = '验证码输入错误'
		elif sub_time(result_phone.last().code_start, result_phone.last().code_end) > 600:#定时600秒
			data['code'] = '203'
			data['msg'] = '验证码超时'
		elif(len(result_user) != 0):
			data['code'] = '204'
			data['msg'] = '该用户名已被注册'
		else:
			user = User()#创建账号信息
			user.identification = data_identification
			user.password = data_password
			user.time_register = timezone.now()
			user.time_login = timezone.now()
			user.save()
			
			content = {}
			content['identification'] = user.identification
			content['nickname'] = string.strip(user.nickname)
			content['sex'] = user.sex
			content['birthday'] = str(user.birthday)
			content['motto'] = string.strip(user.motto)
			content['time'] = second_transfer(user.timing_useful)
			try:
				content['head'] = base_url + user.head.url
			except Exception, e:
				content['head'] = base_url + IMAGE_DEFAULT
			
			data['content'] = content
			data['code'] = '200'
			data['msg'] = '注册成功'
		
		return HttpResponse(simplejson.dumps(data))
		
		
def information_get(request):
#	if request.method == 'GET':
#		flag_identification = '17768345313'
	if request.method == 'POST':
		flag_identification = request.POST['identification']#获取用户名
		
		result = User.objects.filter(identification = flag_identification)
		
		data = {}
		if len(result) == 0:
			data['code'] = '201'
			data['msg'] = '该用户不存在'
		else:
			result = result.last()
			
			content = {}
			content['identification'] = result.identification
			content['nickname'] = string.strip(result.nickname)#去掉后缀的\r\n
			content['sex'] = result.sex
			content['birthday'] = str(result.birthday)
			content['motto'] = string.strip(result.motto)#去掉后缀的\r\n
			content['time'] = second_transfer(result.timing_useful)
			content['num_prize'] = result.num_prize
			try:
				content['head'] = base_url + result.head.url
			except Exception, e:
				content['head'] = base_url + IMAGE_DEFAULT
			
			data['content'] = content
			data['code'] = '200'
			data['msg'] = '个人信息下载成功'
		
		return HttpResponse(simplejson.dumps(data))
		
		
def information_post(request):
	if request.method == 'POST':
		flag_identification = request.POST['identification']#获取用户名
		result = User.objects.filter(identification = flag_identification).last()
		
		data_nickname = request.POST['nickname']#获取昵称
		data_sex = request.POST['sex']#获取性别
		data_birthday = request.POST['birthday']#获取生日
		data_motto = request.POST['motto']#获取签名
		if 'head' in request.FILES:#获取头像
			data_head = request.FILES['head']
		else:
			data_head = None
		
		data={}
		try:
			result.nickname = data_nickname
			result.sex = data_sex
			result.birthday = data_birthday
			result.motto = data_motto
			if data_head != None:
				result.head = data_head
			result.save()
			
			data['code'] = '200'
			data['msg'] = '个人信息修改成功'
		except Exception, e:
			print e
			data['code'] = '201'
			data['msg'] = '个人信息修改失败'
		
		return HttpResponse(simplejson.dumps(data))
		
		
def timing_post(request):
	if request.method == 'POST':
		get_json = simplejson.loads(request.body)
		flag_identification = get_json['identification']#获取用户名
		data_timing = get_json['timing']#获取计时
		for item in data_timing:
			date_start = datetime.strptime(item['date_start'], '%Y-%m-%d')#String转datetime
			date_end= datetime.strptime(item['date_end'], '%Y-%m-%d')
			time_start = datetime.strptime(item['time_start'], '%H:%M:%S')
			time_end = datetime.strptime(item['time_end'], '%H:%M:%S')
			data_number = item['number']#获取蓝牙连接个数
		
			mark, timing_useful = calculate(date_start, date_end, time_start, time_end, flag_identification, data_number)
					
			#将积分存入个人信息
			result = User.objects.filter(identification = flag_identification).last()
			result.mark += mark
			result.timing_useful += timing_useful
			result.save()
			
		data = {}
		data['code'] = '200'
		data['msg'] = '计时成功'
		data['mark'] = mark
			
		return HttpResponse(simplejson.dumps(data))
		
		
def mark_get_days(request):
#	if request.method == 'GET':
#		flag_identification = '15061882150'
#		data_date_start = '2017-3-2'
#		data_date_end = '2017-3-5'
	if request.method == 'POST':
		flag_identification = request.POST['identification']#获取用户名
		data_date_start = request.POST['date_start']#获取起始日期
		data_date_end = request.POST['date_end']#获取结束日期
		
		data_date_start = datetime.strptime(data_date_start, '%Y-%m-%d')#String转datetime
		data_date_end = datetime.strptime(data_date_end, '%Y-%m-%d')#String转datetime
		data_date_end += timedelta(days = 1)#需要提前把结束日期加一天，否则那天不算
		
		result_timing = Timing.objects.filter(identification = flag_identification).all()#先过滤出相应用户名的所有信息
		result_user = User.objects.filter(identification = flag_identification).last()
		
		content = {}
		content['identification'] = flag_identification
		content['time'] = second_transfer(result_user.timing_useful)
		
		while(data_date_start != data_date_end):
			date_index = data_date_start.strftime('%Y-%m-%d')
		
			content_day = {}
			content_day['mark'] = 0#当天总积分初始为0
			time_total = 0#当天总时间初始为0
			all_timing = result_timing.filter(date = data_date_start)#过滤出当天所有的计时
			for j in range(0, len(all_timing)):#计算当天总积分
				content_day['mark'] += all_timing[j].mark
				time_total += all_timing[j].timing_useful
			data_date_start += timedelta(days = 1)#加一天
			content_day['time'] = second_transfer(time_total)
			content[date_index] = content_day#当天总时间
		
		data = {}
		data['content'] = content
		data['code'] = '200'
		data['msg'] = '积分获取成功'
		
		return HttpResponse(simplejson.dumps(data))
		
		
def mark_get_today(request):
#	if request.method == 'GET':
#		flag_identification = '15061882150'
	if request.method == 'POST':
		flag_identification = request.POST['identification']#获取用户名
		
		data_date = mydate.date.today()#获取今天日期
		
		result_timing = Timing.objects.filter(identification = flag_identification).filter(date = data_date)#过滤出当天所有的计时
		result_user = User.objects.filter(identification = flag_identification).last()
		
		content = {}
		content['identification'] = flag_identification
		content['time_total'] = second_transfer(result_user.timing_useful)
		content['mark_total'] = result_user.mark
		
		time_today = 0
		mark_today = 0
		for item in result_timing:#计算当天有效时间/积分
			time_today += item.timing_useful
			mark_today += item.mark
		content['time_today'] = second_transfer(time_today)
		content['mark_today'] = mark_today
		
		data = {}
		data['content'] = content
		data['code'] = '200'
		data['msg'] = '有效时间/积分获取成功'
		
		return HttpResponse(simplejson.dumps(data))
		
		
def shop_list_get(request):
#	if request.method == 'GET':
	if request.method == 'POST':
		result = Shop.objects.all()
		
		data = {}
		if len(result) == 0:
			data['code'] = '201'
			data['msg'] = '当前无商家'
		else:
			content = []
			for item in result:
				shop_item = {}
				shop_item['shop_id'] = item.shop_id
				shop_item['shop_name'] = item.shop_name
				shop_item['shop_address'] = item.shop_address
				shop_item['shop_telephone'] = item.shop_telephone
				try:
					shop_item['shop_image'] = base_url + item.shop_image.url
				except Exception, e:
					shop_item['shop_image'] = base_url + IMAGE_DEFAULT
				shop_item['goods_number'] = len(Goods.objects.filter(shop_name = item.shop_name))
				content.append(shop_item)
				
				data['content'] = content
				data['code'] = '200'
				data['msg'] = '商家列表获取成功'
		
		return HttpResponse(simplejson.dumps(data))
		
		
def goods_list_get(request):
#	if request.method == 'GET':
#		flag_shop_id = '01'
	if request.method == 'POST':
		flag_shop_id = request.POST['shop_id']#获取商家ID
		
		data = {}
		result_temp = Shop.objects.filter(shop_id = flag_shop_id)
		if len(result_temp) == 0:
			data['code'] = '201'
			data['msg'] = '当前商家不存在'
		else:
			
			#带着找出的商家名称去商品表里寻找
			result = Goods.objects.filter(shop_name = result_temp.last().shop_name)
			if len(result) == 0:
				data['code'] = '202'
				data['msg'] = '当前商家无商品'
			else:
				content = []
				for item in result:
					goods_item = {}
					goods_item['goods_id'] = item.goods_id
					goods_item['shop_name'] = item.shop_name
					goods_item['goods_name'] = item.goods_name
					goods_item['goods_information'] = item.goods_information
					goods_item['goods_introduction'] = item.goods_introduction
					try:
						goods_item['goods_image'] = base_url + item.goods_image.url
					except Exception, e:
						goods_item['goods_image'] = base_url + IMAGE_DEFAULT
					goods_item['mark_need'] = item.mark_need
					goods_item['money_need'] = item.money_need
					goods_item['money_origin'] = item.money_origin
					content.append(goods_item)
					
					data['content'] = content
					data['code'] = '200'
					data['msg'] = '商品列表获取成功'
		
		return HttpResponse(simplejson.dumps(data))
		
		
def goods_information_get(request):
#	if request.method == 'GET':
#		flag_goods_id = '0102'
	if request.method == 'POST':
		flag_goods_id = request.POST['goods_id']#获取商品ID
		
		result = Goods.objects.filter(goods_id = flag_goods_id).last()
		
		content = {}
		content['goods_id'] = result.goods_id
		content['shop_name'] = result.shop_name
		content['goods_name'] = result.goods_name
		content['goods_information'] = result.goods_information
		content['goods_introduction'] = result.goods_introduction
		try:
			content['goods_image'] = base_url + result.goods_image.url
		except Exception, e:
			content['goods_image'] = base_url + IMAGE_DEFAULT
		content['mark_need'] = result.mark_need
		content['money_need'] = result.money_need
		content['money_origin'] = result.money_origin
		
		data = {}
		data['content'] = content
		data['code'] = '200'
		data['msg'] = '商品信息获取成功'
		
		return HttpResponse(simplejson.dumps(data))
		
		
def discount_buy(request):
#	if request.method == 'GET':
#		flag_identification = '15061882150'
#		flag_goods_id = '0102'
#		data_goods_amount = '3'
	if request.method == 'POST':
		flag_identification = request.POST['identification']#获取用户名
		flag_goods_id = request.POST['goods_id']#获取商品ID
		data_goods_amount = request.POST['goods_amount']#获取购买数量
		
		result_user = User.objects.filter(identification = flag_identification).last()
		result_goods = Goods.objects.filter(goods_id = flag_goods_id).last()
		data_goods_amount = int(data_goods_amount)
		
		data = {}
		if result_user.mark - result_goods.mark_need * data_goods_amount < 0:
			data['code'] = '201'
			data['msg'] = '对不起，您的剩余积分不足！'
		else:
			result_user.mark -= result_goods.mark_need * data_goods_amount#现在的积分等于你购买优惠券后的剩余积分
			result_user.save()
			
			#下面是创造优惠券部分
			for i in range(0, data_goods_amount):
				discount = Discount()
				discount.identification = result_user.identification
				discount.goods_id = result_goods.goods_id
				discount.shop_name = result_goods.shop_name
				discount.goods_name = result_goods.goods_name
				discount.goods_information = result_goods.goods_information
				discount.goods_introduction = result_goods.goods_introduction
				discount.goods_image = result_goods.goods_image
				discount.mark_need = result_goods.mark_need
				discount.money_need = result_goods.money_need
				discount.time_buy = timezone.now()
				discount.money_origin = result_goods.money_origin
				discount.status = 1
				discount.save()
			
			data['code'] = '200'
			data['msg'] = '商品优惠券购买成功'
		
		content = {}
		content['identification'] = flag_identification
		content['goods_id'] = flag_goods_id
		content['mark_used'] = result_goods.mark_need * data_goods_amount#你此次花去的积分
		content['mark_remained'] = result_user.mark#表示你剩余的积分
		data['content'] = content
		
		return HttpResponse(simplejson.dumps(data))
		
		
def discount_list_get(request):
#	if request.method == 'GET':
#		flag_identification = '15061882150'
	if request.method == 'POST':
		flag_identification = request.POST['identification']#获取用户名
		
		result = Discount.objects.filter(identification = flag_identification).filter(status = 1)
		
		data = {}
		if len(result) == 0:
			data['code'] = '201'
			data['msg'] = '您当前没有优惠券'
		else:
			content = []
			for item in result:
				discount_item = {}
				discount_item['id'] = item.id
				discount_item['goods_id'] = item.goods_id
				discount_item['shop_name'] = item.shop_name
				discount_item['goods_name'] = item.goods_name
				discount_item['goods_information'] = item.goods_information
				discount_item['goods_introduction'] = item.goods_introduction
				try:
					discount_item['goods_image'] = base_url + item.goods_image.url
				except Exception, e:
					discount_item['goods_image'] = base_url + IMAGE_DEFAULT
				discount_item['mark_need'] = item.mark_need
				discount_item['money_need'] = item.money_need
				discount_item['money_origin'] = item.money_origin
				discount_item['status'] = 1
				content.append(discount_item)
				
			data['content'] = content
			data['code'] = '200'
			data['msg'] = '“我的优惠”列表获取成功'
				
		return HttpResponse(simplejson.dumps(data))
		
		
def buy_list_get(request):
#	if request.method == 'GET':
#		flag_identification = '15061882150'
	if request.method == 'POST':
		flag_identification = request.POST['identification']#获取用户名
		
		result_0 = Discount.objects.filter(identification = flag_identification).filter(status = 0)#0代表已使用
		result_1 = Discount.objects.filter(identification = flag_identification).filter(status = -1)#-1代表已过期
		
		data = {}
		if len(result_0) == 0 and len(result_1) == 0:
			data['code'] = '201'
			data['msg'] = '您当前没有购买记录'
		else:
			content = []
			for item in result_0:
				discount_item = {}
				discount_item['id'] = item.id
				discount_item['goods_id'] = item.goods_id
				discount_item['shop_name'] = item.shop_name
				discount_item['goods_name'] = item.goods_name
				discount_item['goods_information'] = item.goods_information
				discount_item['goods_introduction'] = item.goods_introduction
				try:
					discount_item['goods_image'] = base_url + item.goods_image.url
				except Exception, e:
					discount_item['goods_image'] = base_url + IMAGE_DEFAULT
				discount_item['mark_need'] = item.mark_need
				discount_item['money_need'] = item.money_need
				discount_item['money_origin'] = item.money_origin
				discount_item['status'] = item.status
				content.append(discount_item)
			for item in result_1:
				discount_item = {}
				discount_item['id'] = item.id
				discount_item['goods_id'] = item.goods_id
				discount_item['shop_name'] = item.shop_name
				discount_item['goods_name'] = item.goods_name
				discount_item['goods_information'] = item.goods_information
				discount_item['goods_introduction'] = item.goods_introduction
				try:
					discount_item['goods_image'] = base_url + item.goods_image.url
				except Exception, e:
					discount_item['goods_image'] = base_url + IMAGE_DEFAULT
				discount_item['mark_need'] = item.mark_need
				discount_item['money_need'] = item.money_need
				discount_item['money_origin'] = item.money_origin
				discount_item['status'] = item.status
				content.append(discount_item)
				
			data['content'] = content
			data['code'] = '200'
			data['msg'] = '“我的购买记录”列表获取成功'
				
		return HttpResponse(simplejson.dumps(data))
		
		
def discount_use(request):
#	if request.method == 'GET':
#		flag_identification = '15061882150'
#		flag_id = '32'
	if request.method == 'POST':
		flag_identification = request.POST['identification']#获取用户名
		flag_id = request.POST['id']#获取商品ID
		
		result = Discount.objects.filter(identification = flag_identification).filter(status = 1).filter(id = flag_id).last()
		result.status = 0
		result.time_use = timezone.now()
		result.save()
		
		data = {}
		data['code'] = '200'
		data['msg'] = '优惠券使用成功'
				
		return HttpResponse(simplejson.dumps(data))
		
		
def daily_sign_in(request):
#	if request.method == 'GET':
#		flag_identification = '15061882150'
	if request.method == 'POST':
		flag_identification = request.POST['identification']#获取用户名
		
		result = User.objects.filter(identification = flag_identification).last()
		date_today = mydate.date.today()
		
		data = {}
		#今天签过到的情况
		if (date_today - result.date_sign_in).days == 0:
			data['code'] = '201'
			data['msg'] = '您今天已经签到过了'
		else:
			#断签的情况
			if (date_today - result.date_sign_in).days != 1:
				result.date_sign_in = date_today
				result.day_sign_in = 1
				result.mark_sign_in += 1
				result.save()
			#连续签到的情况
			else:
				result.date_sign_in = date_today
				result.day_sign_in += 1
				if result.day_sign_in >= 5:
					result.mark_sign_in += 5
				else:
					result.mark_sign_in += result.day_sign_in
				result.save()
			
			data['code'] = '200'
			data['msg'] = '签到成功'
			
		content = {}
		content['mark_sign_in'] = result.mark_sign_in
		content['day_sign_in'] = result.day_sign_in
		data['content'] = content
				
		return HttpResponse(simplejson.dumps(data))
		
		
def friend_list_get(request):
#	if request.method == 'GET':
#		flag_identification = '15061882150'
	if request.method == 'POST':
		flag_identification = request.POST['identification']#获取用户名
		
		result_friend = Friend.objects.filter(identification_sender = flag_identification).filter(status = 0)
		
		data = {}
		if len(result_friend) == 0:
			data['code'] = '201'
			data['msg'] = '当前无好友'
		else:
			content = []
			for item in result_friend:
				friend_item = {}
				friend_item['identification'] = item.identification_receiver
				
				result_user = User.objects.filter(identification = item.identification_receiver).last()
				friend_item['nickname'] = string.strip(result_user.nickname)
				friend_item['sex'] = result_user.sex
				friend_item['birthday'] = str(result_user.birthday)
				friend_item['motto'] = string.strip(result_user.motto)
				friend_item['mark'] = result_user.mark
				try:
					friend_item['head'] = base_url + result_user.head.url
				except Exception, e:
					friend_item['head'] = base_url + IMAGE_DEFAULT
				content.append(friend_item)
				
				data['content'] = content
				data['code'] = '200'
				data['msg'] = '好友列表获取成功'
				
		return HttpResponse(simplejson.dumps(data))
		
		
def friend_add_list_sender(request):
#	if request.method == 'GET':
#		flag_identification = '15061882150'
	if request.method == 'POST':
		flag_identification = request.POST['identification_sender']#获取用户名
		
		result_friend = Friend.objects.filter(identification_sender = flag_identification).filter(status = 1)
		
		data = {}
		if len(result_friend) == 0:
			data['code'] = '201'
			data['msg'] = '当前无好友请求'
		else:
			content = []
			for item in result_friend:
				friend_item = {}
				friend_item['identification'] = item.identification_receiver
				friend_item['status'] = item.status
				
				result_user = User.objects.filter(identification = item.identification_receiver).last()
				friend_item['nickname'] = string.strip(result_user.nickname)
				friend_item['mark'] = result_user.mark
				try:
					friend_item['head'] = base_url + result_user.head.url
				except Exception, e:
					friend_item['head'] = base_url + IMAGE_DEFAULT
				content.append(friend_item)
				
				data['content'] = content
				data['code'] = '200'
				data['msg'] = '“发送的好友请求列表”获取成功'
				
		return HttpResponse(simplejson.dumps(data))
		
		
def friend_add_list_receiver(request):
#	if request.method == 'GET':
#		flag_identification = '15061882150'
	if request.method == 'POST':
		flag_identification = request.POST['identification_receiver']#获取用户名
		
		result_friend = Friend.objects.filter(identification_receiver = flag_identification).filter(status = 1)
		
		data = {}
		if len(result_friend) == 0:
			data['code'] = '201'
			data['msg'] = '当前无好友请求'
		else:
			content = []
			for item in result_friend:
				friend_item = {}
				friend_item['identification'] = item.identification_sender
				friend_item['status'] = item.status
				
				result_user = User.objects.filter(identification = item.identification_sender).last()
				friend_item['nickname'] = string.strip(result_user.nickname)
				friend_item['mark'] = result_user.mark
				try:
					friend_item['head'] = base_url + result_user.head.url
				except Exception, e:
					friend_item['head'] = base_url + IMAGE_DEFAULT
				content.append(friend_item)
				
				data['content'] = content
				data['code'] = '200'
				data['msg'] = '“接收的好友请求列表”获取成功'
				
		return HttpResponse(simplejson.dumps(data))
		
		
def friend_add_request(request):
#	if request.method == 'GET':
#		flag_identification_sender = '15061882150'
#		flag_identification_receiver = '17768345313'
	if request.method == 'POST':
		flag_identification_sender = request.POST['identification_sender']
		flag_identification_receiver = request.POST['identification_receiver']
		
		result_friend = Friend.objects.filter(identification_sender = flag_identification_sender).filter(identification_receiver = flag_identification_receiver)
		result_user = User.objects.filter(identification = flag_identification_receiver)
		
		data = {}
		if len(result_friend) != 0:
			if result_friend.last().status == 1:
				data['code'] = '201'
				data['msg'] = '已发送过该好友请求'
			if result_friend.last().status == 0:
				data['code'] = '202'
				data['msg'] = '对方已经是您的好友'
		
		if len(result_friend) == 0 or result_friend.last().status == -1:
			if len(result_user) == 0:
				data['code'] = '203'
				data['msg'] = '该用户不存在'
			elif cmp(flag_identification_sender, flag_identification_receiver) == 0:
				data['code'] = '204'
				data['msg'] = '不能添加自己为好友'
			else:
				friend = Friend()
				friend.identification_sender = flag_identification_sender
				friend.identification_receiver = flag_identification_receiver
				friend.time_request = timezone.now()
				friend.status = 1
				friend.save()
				
				data['code'] = '200'
				data['msg'] = '已成功发送好友请求'
				
		return HttpResponse(simplejson.dumps(data))
		
		
def friend_add_response(request):
#	if request.method == 'GET':
#		flag_identification_receiver = '17768345313'
#		flag_identification_sender = '15061882150'
#		data_status = '0'
	if request.method == 'POST':
		flag_identification_receiver = request.POST['identification_receiver']
		flag_identification_sender = request.POST['identification_sender']
		data_status = request.POST['status']
		
		result = Friend.objects.filter(identification_sender = flag_identification_sender).filter(identification_receiver = flag_identification_receiver).last()
		
		data = {}
		if result.status == 0:
			data['code'] = '201'
			data['msg'] = '对方已经是您的好友'
		else:
			result.status = data_status
			result.time_response = timezone.now()
			result.save()
			
			#如果对方同意加好友，则双方互为好友
			if data_status == '0':
				friend = Friend()
				friend.identification_sender = result.identification_receiver
				friend.identification_receiver = result.identification_sender
				friend.time_request = result.time_request
				friend.time_response = result.time_response
				friend.status = 0
				friend.save()
			
			data['code'] = '200'
			data['msg'] = '已成功回应对方的请求'
				
		return HttpResponse(simplejson.dumps(data))
		
		
def friend_rank_list_get(request):
#	if request.method == 'GET':
#		flag_identification = '15061882150'
	if request.method == 'POST':
		flag_identification = request.POST['identification']
		
		result_friend = Friend.objects.filter(identification_sender = flag_identification).filter(status = 0)
		
		data = {}
		if len(result_friend) == 0:
			data['code'] = '201'
			data['msg'] = '当前无好友'
		else:
			rank = []
			#针对于每个好友，计算其当天获得积分
			for item_friend in result_friend:
				data_date = mydate.date.today()#获取今天日期
				result_timing = Timing.objects.filter(identification = item_friend.identification_receiver).filter(date = data_date)#过滤出当天所有的计时
				
				#计算当天总积分
				mark_today = 0
				for item_timing in result_timing:
					mark_today += item_timing.mark
				
				#将{好友：积分}存入list
				dic = {}
				dic[item_friend.identification_receiver] = mark_today
				rank.append(dic)
				
			#把自己也加入好友排名
			data_date = mydate.date.today()#获取今天日期
			result_timing = Timing.objects.filter(identification = flag_identification).filter(date = data_date)#过滤出当天所有的计时
			#计算当天总积分
			mark_today = 0
			for item_timing in result_timing:
				mark_today += item_timing.mark
			#把{自己：积分}也存入list
			dic = {}
			dic[flag_identification] = mark_today
			rank.append(dic)
				
			#按当天积分进行排序（冒泡）
			for i in range(0, len(rank)):
				for j in range(0, len(rank) - i - 1):
					if int(rank[j].values()[0]) < int(rank[j + 1].values()[0]):
						t = rank[j]
						rank[j] = rank[j + 1]
						rank[j + 1] = t
			#print rank
			
			#返回已排序的好友积分列表
			num = 0
			content = []
			for item in rank:
				result_user = User.objects.filter(identification = item.keys()[0]).last()
				num += 1
				
				item_rank = {}
				item_rank['identification'] = result_user.identification
				item_rank['nickname'] = string.strip(result_user.nickname)
				item_rank['sex'] = result_user.sex
				item_rank['birthday'] = str(result_user.birthday)
				item_rank['motto'] = string.strip(result_user.motto)
				item_rank['mark'] = item.values()[0]
				item_rank['place'] = num
				try:
					item_rank['head'] = base_url + result_user.head.url
				except Exception, e:
					item_rank['head'] = base_url + IMAGE_DEFAULT
				content.append(item_rank)
			
			data['content'] = content
			data['code'] = '200'
			data['msg'] = '“好友积分排名列表”获取成功'
		
		return HttpResponse(simplejson.dumps(data))
		
		
def advertisement_list_get(request):
#	if request.method == 'GET':
	if request.method == 'POST':
		result = Advertisement.objects.all()
		
		data = {}
		if len(result) == 0:
			data['code'] = '201'
			data['msg'] = '当前无广告'
		else:
			content = []
			for item in result:
				advertisement_item = {}
				advertisement_item['words'] = item.words
				try:
					advertisement_item['image'] = base_url + item.image.url
				except Exception, e:
					advertisement_item['image'] = base_url + IMAGE_DEFAULT
				content.append(advertisement_item)
				
				data['content'] = content
				data['code'] = '200'
				data['msg'] = '广告列表获取成功'
		
		return HttpResponse(simplejson.dumps(data))
		
		
def prize_list_get(request):
#	if request.method == 'GET':
	if request.method == 'POST':
		result = Prize.objects.all()
		
		data = {}
		if len(result) == 0:
			data['code'] = '201'
			data['msg'] = '当前无奖品'
		else:
			content = []
			for item in result:
				prize_item = {}
				prize_item['words'] = item.words
				prize_item['id'] = item.id
				content.append(prize_item)
				
				data['content'] = content
				data['code'] = '200'
				data['msg'] = '奖品列表获取成功'
		
		return HttpResponse(simplejson.dumps(data))
		
		
def prize_get(request):
#	if request.method == 'GET':
#		flag_identification = '15061882150'
	if request.method == 'POST':
		flag_identification = request.POST['identification']
		
		result_user = User.objects.filter(identification = flag_identification).last()
		result_prize = Prize.objects.all()
		
		data = {}
		if result_user.num_prize <= 0:
			data['code'] = '201'
			data['msg'] = '您的抽奖次数不足'
		else:
			'''
			抽奖概率算法，决定多少概率抽中哪一个
			奖品1：1%
			奖品2：3%
			奖品3：6%
			奖品4：10%
			奖品5：30%
			奖品6：50%
			'''
			RAND = random.randint(1, 100)
			if RAND == 1:
				prize = result_prize[0]
			elif RAND <= 4:
				prize = result_prize[1]
			elif RAND <= 10:
				prize = result_prize[2]
			elif RAND <= 20:
				prize = result_prize[3]
			elif RAND <= 50:
				prize = result_prize[4]
			else:
				prize = result_prize[5]

			#用户的抽奖次数-1
			result_user.num_prize -= 1
			result_user.save()
			
			content = {}
			content['words'] = prize.words
			content['id'] = prize.id
			
			data['content'] = content
			data['code'] = '200'
			data['msg'] = '抽奖成功'
			
		return HttpResponse(simplejson.dumps(data))
		
		
def prize_num_buy(request):
#	if request.method == 'GET':
#		flag_identification = '17768345313'
#		data_num_prize = '3'
	if request.method == 'POST':
		flag_identification = request.POST['identification']#获取用户名
		data_num_prize = request.POST['num_prize']#获取 需要购买的抽奖次数
		data_num_prize = int(data_num_prize)#将data_num_prize转换为整型
		
		result = User.objects.filter(identification = flag_identification).last()
		mark_need = PRIZE_PERCENT * data_num_prize#计算购买这些抽奖次数所需要的积分
		
		data = {}
		if result.mark <= mark_need:
			data['code'] = '201'
			data['msg'] = '您的积分不足'
		else:
			#用户的抽奖次数相应增加，积分相应减少
			result.num_prize += data_num_prize
			result.mark -= mark_need
			result.save()
			
			data['code'] = '200'
			data['msg'] = '购买抽奖次数成功'
			
		return HttpResponse(simplejson.dumps(data))
		

def card_search(request):
#	if request.method == 'GET':
#		flag_number = '1030614435'
	if request.method == 'POST':
		flag_number = request.POST['number']#获取学号
		
		data = {}
		data['code'] = '201'
		data['msg'] = '未查询到该学号'

		xlsfile = r'data/info.xlsx'
		book = xlrd.open_workbook(xlsfile)#获得excel的book对象
		sheet = book.sheet_by_index(0)#通过sheet索引获得sheet对象
		for i in range(1, sheet.nrows):
			cell_value = int(sheet.cell_value(i, 0))#通过cell的位置坐标获得指定cell的值
			if cell_value == int(flag_number):
				data['code'] = '200'
				data['msg'] = '获取成功'

				content = {}
				content['name'] = sheet.cell_value(i, 1)
				content['school'] = sheet.cell_value(i, 2)
				content['major'] = sheet.cell_value(i, 3)
				content['class'] = sheet.cell_value(i, 4)
				content['sex'] = sheet.cell_value(i, 5)
				data['content'] = content
				break

		return HttpResponse(simplejson.dumps(data))


def qrcode_make(request):
#	if request.method == 'GET':
	if request.method == 'POST':
		
		qr = qrcode.QRCode(version = 1, box_size = 10, border = 4)
		qr.add_data('支付成功')
		qr.make(fit = True)
		img = qr.make_image()
		img.save('static/advanceduse.png')

		content = {}
		content['qrcode'] = base_url + 'static/advanceduse.png'
		data = {}
		data['code'] = '200'
		data['msg'] = '二维码生成成功'
		data['content'] = content
		
		return HttpResponse(simplejson.dumps(data))


def APP_download(request):
	def file_iterator(file_name, chunk_size=512):
		with open(file_name) as f:
			while True:
				c = f.read(chunk_size)
				if c:
					yield c
				else:
					break

	the_file_name = 'APP/md.apk'
	response = StreamingHttpResponse(file_iterator(the_file_name))
	response['Content-Type'] = 'application/octet-stream'
	response['Content-Length'] = os.path.getsize(the_file_name)
	response['Content-Disposition'] = 'attachment;filename="{0}"'.format(the_file_name)
	
	return response
	
	
def version_update(request):
#	if request.method == 'GET':
#		flag_version_now = '2.2'
	if request.method == 'POST':
		flag_version_now = request.POST['version_now']#获取用户名
		
		data = {}
		if float(flag_version_now) == VERSION_LATEST:
			data['code'] = '200'
			data['msg'] = '当前版本已经是最新版本'
		else:
			content = {}
			content['version_latest'] = base_url + 'miandui/APP_download/'
			data['content'] = content
			data['code'] = '201'
			data['msg'] = '检测到最新版本，即将更新'
			
		return HttpResponse(simplejson.dumps(data))


def login_2(request):
#	if request.method == 'GET':
#		data_identification = '15150147508'#获取用户名
#		data_password = 'qjzhzw'#获取密码
	if request.method == 'POST':
		data_identification = request.POST['identification']#获取用户名
		data_password = request.POST['password']#获取密码
		
		result_shop = Shop.objects.filter(identification = data_identification)
		
		data = {}
		if len(result_shop) == 0:
			data['code'] = '201'
			data['msg'] = '该用户名不存在'
		elif cmp(result_shop.last().password, data_password) != 0:
			data['code'] = '202'
			data['msg'] = '密码输入错误'
		else:
			result = result_shop.last()
			#更新最后登录时间
			result.time_login = timezone.now()
			result.save()

			data['code'] = '200'
			data['msg'] = '登录成功'
		
		return HttpResponse(simplejson.dumps(data))


def register_2(request):
#	if request.method == 'GET':
#		data_identification = '15150147508'#获取用户名
#		data_shop_name = '111'#获取商店名称
#		data_password = 'qjzhzw'#获取密码
	if request.method == 'POST':
		data_identification = request.POST['identification']#获取用户名
		data_shop_name = request.POST['shop_name']#获取商店名称
		data_password = request.POST['password']#获取密码
		
		result_shop = Shop.objects.filter(identification = data_identification)
		
		data = {}
		if len(result_shop) != 0:
			data['code'] = '201'
			data['msg'] = '该用户名已被注册'
		else:
			shop = Shop()#创建账号信息
			shop.identification = data_identification
			shop.shop_name = data_shop_name
			shop.password = data_password
			shop.time_register = timezone.now()
			shop.save()
			
			data['code'] = '200'
			data['msg'] = '注册成功'
		
		return HttpResponse(simplejson.dumps(data))


def forget_vertification_2(request):
#	if request.method == 'GET':
#		data_identification = '15150147508'
	if request.method == 'POST':
		data_identification = request.POST['identification']#获取用户名
		
		result = Shop.objects.filter(identification = data_identification)
		
		data = {}
		if len(result) == 0:
			data['code'] = '201'
			data['msg'] = '该用户名不存在'
		else:
			get_code = sms.send(data_identification)#发送验证码
			
			phone = Phone()#创建手机号信息
			phone.identification = data_identification
			phone.code = get_code
			phone.code_start = time.strftime('%H:%M:%S',time.localtime(time.time()))#记录当前时间
			phone.save()
			
			data['code'] = '200'
			data['msg'] = '短信发送成功'
		
		return HttpResponse(simplejson.dumps(data))
		
		
def forget_login_2(request):
#	if request.method == 'GET':
#		data_identification = '15150147508'#获取用户名
#		data_code = '685042'#获取验证码
	if request.method == 'POST':
		data_identification = request.POST['identification']#获取用户名
		data_code = request.POST['code']#获取验证码
		
		result_phone = Phone.objects.filter(identification = data_identification)
		result_shop = Shop.objects.filter(identification = data_identification)
		
		#记录当前时间
		try:
			result = result_phone.last()
			result.code_end = time.strftime('%H:%M:%S',time.localtime(time.time()))#记录当前时间
			result.save()
		except Exception, e:
			print e
		
		data = {}
		if len(result_phone) == 0:
			data['code'] = '201'
			data['msg'] = '尚未发送验证码'
		elif cmp(result_phone.last().code, data_code) != 0:
			data['code'] = '202'
			data['msg'] = '验证码输入错误'
		elif sub_time(result_phone.last().code_start, result_phone.last().code_end) > 600:#定时600秒
			data['code'] = '203'
			data['msg'] = '验证码超时'
		elif len(result_shop) == 0:
			data['code'] = '204'
			data['msg'] = '该用户名不存在'
		else:
			result = result_shop.last()
			#更新最后登录时间
			result.time_login = timezone.now()
			result.save()

			data['code'] = '200'
			data['msg'] = '登陆成功'
		
		return HttpResponse(simplejson.dumps(data))


def order_list_get_2(request):
#	if request.method == 'GET':
#		flag_identification = '1'
	if request.method == 'POST':
		flag_identification = request.POST['identification']#获取用户名

		result_order = Order.objects.filter(identification = flag_identification).all()
		result_temp = OrderGoods.objects.filter(identification = flag_identification).all()

		data = {}
		if len(result_order) == 0:
			data['code'] = '201'
			data['msg'] = '当前账号无订单'
		else:
			content = []
			for item in result_order:
				order_item = {}
				try:
					order_item['nickname'] = User.objects.filter(identification = item.phone).last().nickname
				except:
					order_item['nickname'] = '不存在'
				order_item['phone'] = item.phone
				order_item['time_arrive'] = str(item.time_arrive.strftime('%m-%d %H:%M'))
				order_item['money_discount'] = item.money_discount
				order_item['money_service'] = item.money_service
				order_item['status'] = item.status

				result_goods = result_temp.filter(phone = item.phone)
				goods = []
				for item2 in result_goods:
					goods_item = {}
					goods_item['goods_name'] = item2.goods_name
					goods_item['goods_number'] = item2.goods_number
					goods_item['money_need'] = item2.money_need
					goods.append(goods_item)
				order_item['goods'] = goods
				content.append(order_item)

			data['code'] = '200'
			data['msg'] = '订单信息获取成功'
			data['content'] = content
			
		return HttpResponse(simplejson.dumps(data))
		
		
def qrcode_make_2(request):
#	if request.method == 'GET':
	if request.method == 'POST':
		
		qr = qrcode.QRCode(version = 1, box_size = 10, border = 4)
		qr.add_data('用户消费成功')
		qr.make(fit = True)
		img = qr.make_image()
		img.save('static/advanceduse2.png')

		content = {}
		content['qrcode'] = base_url + 'static/advanceduse2.png'
		data = {}
		data['code'] = '200'
		data['msg'] = '二维码生成成功'
		data['content'] = content
		
		return HttpResponse(simplejson.dumps(data))


#计算时间差
def sub_time(time_start, time_end):
	hour_start = time_start.hour
	minute_start = time_start.minute
	second_start = time_start.second
	hour_end = time_end.hour
	minute_end = time_end.minute
	second_end = time_end.second
	
	start = hour_start * 60 * 60 + minute_start * 60 + second_start
	end = hour_end * 60 * 60 + minute_end * 60 + second_end
	
	return end - start
	
	
#由秒数计算 小时数/分钟数/秒数
def second_transfer(timing_useful):
	hour = timing_useful / (60 * 60)
	minute  = (timing_useful - hour * (60 * 60)) / 60
	second = timing_useful % 60
	
	hour = str(hour)
	minute = str(minute)
	second = str(second)
	
	if len(minute) == 1:
		minute = '0' + minute
	if len(second) == 1:
		second = '0' + second
	
	return hour + ':' + minute + ':' + second
	
	
#保存计时，并计算/返回 有效时间和积分
def calculate(date_start, date_end, time_start, time_end, flag_identification, data_number):
	date_delta = date_end - date_start#计算日期间隔
	mark = 0
	timing_useful = 0
			
	if date_delta.days == 0:
		timing = Timing()
		timing.identification = flag_identification
		timing.date = date_start
		timing.number = data_number
		timing.time_start = time_start
		timing.time_end = time_end
		time_real = judge_single(date_start, time_start, time_end, flag_identification, data_number)#计算实际有效时间
		timing.timing_useful = time_real#计算有效时间
		#print timing.timing_useful
		#print MARK_PERCENT
		#print data_number
		timing.mark = float(timing.timing_useful) * MARK_PERCENT * float(data_number)#计算积分
		if int(timing.mark) > 0:#只有计时有效（即该阶段获得积分不为0才算有效）
			timing.save()
			mark += timing.mark
			timing_useful += timing.timing_useful
		
	if date_delta.days == 1:
		timing1 = Timing()
		timing1.identification = flag_identification
		timing1.date = date_start
		timing1.number = data_number
		timing1.time_start = time_start
		timing1.time_end = datetime.strptime('23:59:59', '%H:%M:%S')
		time_real = judge_single(date_start, time_start, time_end, flag_identification, data_number)#计算实际有效时间
		timing1.timing_useful = time_real#计算有效时间
		timing1.mark = float(timing1.timing_useful) * MARK_PERCENT * float(data_number)#计算积分
		if int(timing1.mark) > 0:#只有计时有效（即该阶段获得积分不为0才算有效）
			timing1.save()
			mark += timing1.mark
			timing_useful += timing1.timing_useful
		
		timing2 = Timing()
		timing2.identification = flag_identification
		timing2.date = date_end
		timing2.number = data_number
		timing2.time_start = datetime.strptime('0:0:0', '%H:%M:%S')
		timing2.time_end = time_end
		time_real = judge_single(date_end, time_start, time_end, flag_identification, data_number)#计算实际有效时间
		timing2.timing_useful = time_real#计算有效时间
		timing2.mark = float(timing2.timing_useful) * MARK_PERCENT * float(data_number)#计算积分
		if int(timing2.mark) > 0:#只有计时有效（即该阶段获得积分不为0才算有效）
			timing2.save()
			mark += timing2.mark
			timing_useful += timing2.timing_useful
		
	return mark, timing_useful
	
	
#实际时间计算方式（主要是单人要单独拿出来算）
def judge_single(date_start, time_start, time_end, flag_identification, data_number):
	#单人每日积分有上限
	if data_number == 1:
		#找出对应ID当日通过单人模式获得的总积分
		result_timing = Timing.objects.filter(identification = flag_identification).filter(date = date_start).filter(number = 1)
		time_today = 0
		for item in result_timing:#计算当天有效时间/积分
			time_today += item.timing_useful
			
		#1.已经达到积分上限的情况
		if time_today >= TIME_MAX:
			time_real = 0
		#2.部分达到积分上限的情况
		elif time_today + sub_time(time_start, time_end) >= TIME_MAX:
			time_real = TIME_MAX - time_today
		#3.未达到积分上限的情况
		else:
			time_real = sub_time(time_start, time_end)
	else:
		time_real = sub_time(time_start, time_end)
		
	return time_real


# Create your views here.
