# *-* coding: utf-8 *-*

from __future__ import unicode_literals

from django.db import models

import datetime

class User(models.Model):
	identification = models.IntegerField('账号')
	password = models.CharField('密码', max_length = 20)
	nickname = models.CharField('昵称', max_length = 20, default = '您尚未设置昵称')
	sex = models.CharField('性别', max_length = 20, default = '男')
	birthday = models.DateField('生日', default = '1970-1-1')
	motto = models.CharField('签名', max_length = 20, default = '您尚未设置签名')
	head = models.FileField('头像', upload_to = 'static/head')
	mark = models.IntegerField('积分',  default = 0)
	timing_useful = models.IntegerField('有效秒数',  default = 0)
	time_login = models.DateTimeField('最后登录时间', default = datetime.datetime(1970, 1, 1, 0, 0, 0))
	time_register = models.DateTimeField('注册时间', default = datetime.datetime(1970, 1, 1, 0, 0, 0))
	date_sign_in = models.DateField('最近签到日期', default = datetime.date(1970, 1, 1))
	day_sign_in = models.IntegerField('已连续签到天数',  default = 0)
	mark_sign_in = models.IntegerField('签到获得积分',  default = 0)
	num_prize = models.IntegerField('抽奖次数', default = 0)
	def __unicode__(self):
		return str(self.identification)
	class Meta:
		verbose_name = '用户信息'
		verbose_name_plural = '用户信息'
		
class Phone(models.Model):
	identification = models.IntegerField('手机号')
	code = models.CharField('验证码', max_length = 6)
	code_start = models.TimeField('验证码起始时间', null = True)
	code_end = models.TimeField('验证码结束时间', null = True)
	def __unicode__(self):
		return str(self.identification)
	class Meta:
		verbose_name = '手机验证码'
		verbose_name_plural = '手机验证码'
		
class Timing(models.Model):
	identification = models.IntegerField('账号')
	time_start = models.TimeField('计时起始时间', null = True)
	time_end = models.TimeField('计时结束时间', null = True)
	timing_useful = models.IntegerField('有效秒数',  default = 0)
	date = models.DateField('日期', null = True)
	mark = models.IntegerField('积分',  default = 0)
	number = models.IntegerField('蓝牙连接个数', default = 0)
	def __unicode__(self):
		return str(self.identification)
	class Meta:
		verbose_name = '计时信息'
		verbose_name_plural = '计时信息'
		
class Shop(models.Model):
	identification = models.IntegerField('账号')
	password = models.CharField('密码', max_length = 20)
	shop_id = models.CharField('商家ID', max_length = 4)
	shop_name = models.CharField('商家名称', max_length = 20)
	shop_address = models.CharField('商家地址', max_length = 100)
	shop_telephone = models.CharField('联系电话', max_length = 20)
	shop_image = models.FileField('商家图片', upload_to = 'static/shop')
	time_register = models.DateTimeField('注册时间', default = datetime.datetime(1970, 1, 1, 0, 0, 0))
	def __unicode__(self):
		return str(self.shop_id)
	class Meta:
		verbose_name = '商家信息'
		verbose_name_plural = '商家信息'

class Goods(models.Model):
	goods_id = models.CharField('商品ID', max_length = 4)
	shop_name = models.CharField('商家名称', max_length = 20)
	goods_name = models.CharField('商品名称', max_length = 20)
	goods_information = models.CharField('商品信息', max_length = 100)
	goods_introduction = models.CharField('使用说明', max_length = 100)
	goods_image = models.FileField('商品图片', upload_to = 'static/goods')
	mark_need = models.IntegerField('所需积分')
	money_need = models.CharField('所需金钱', max_length = 10)
	money_origin = models.CharField('原价', max_length = 10)
	goods_number = models.IntegerField('商品数量', default = 999, null = True)
	def __unicode__(self):
		return str(self.goods_id)
	class Meta:
		verbose_name = '商品信息'
		verbose_name_plural = '商品信息'
		
class Discount(models.Model):
	identification = models.IntegerField('账号')
	goods_id = models.CharField('商品ID', max_length = 4)
	shop_name = models.CharField('商家名称', max_length = 20)
	goods_name = models.CharField('商品名称', max_length = 20)
	goods_information = models.CharField('商品信息', max_length = 100)
	goods_introduction = models.CharField('使用说明', max_length = 100)
	goods_image = models.FileField('商品图片', upload_to = 'static/goods')
	mark_need = models.IntegerField('所需积分')
	money_need = models.CharField('所需金钱', max_length = 10)
	money_origin = models.CharField('原价', max_length = 10)
	status = models.IntegerField('状态', default = 1)
	time_buy = models.DateTimeField('购买时间', null = True)
	time_use = models.DateTimeField('使用时间', null = True)
	def __unicode__(self):
		return str(self.identification)
	class Meta:
		verbose_name = '抵用券信息'
		verbose_name_plural = '抵用券信息'
		
class Friend(models.Model):
	identification_sender = models.IntegerField('发送者账号')
	identification_receiver = models.IntegerField('接收者账号')
	time_request = models.DateTimeField('好友申请发送时间', null = True)
	time_response = models.DateTimeField('好友申请处理时间', null = True)
	status = models.IntegerField('状态', default = 1)
	def __unicode__(self):
		return str(self.identification_sender)
	class Meta:
		verbose_name = '好友信息'
		verbose_name_plural = '好友信息'
		
class Advertisement(models.Model):
	words = models.CharField('广告说明', max_length = 100)
	image = models.FileField('广告图片', upload_to = 'static/advertisement')
	def __unicode__(self):
		return self.words
	class Meta:
		verbose_name = '广告信息'
		verbose_name_plural = '广告信息'
		
class Prize(models.Model):
	words = models.CharField('奖品名称', max_length = 20)
	def __unicode__(self):
		return self.words
	class Meta:
		verbose_name = '抽奖信息'
		verbose_name_plural = '抽奖信息'

class Order(models.Model):
	identification = models.IntegerField('账号')
	phone = models.IntegerField('手机号')
	time_arrive = models.DateTimeField('（预计）到达时间', null = True)
	money_discount = models.CharField('商家活动优惠', max_length = 10)
	money_service = models.CharField('平台服务费', max_length = 10)
	status = models.IntegerField('状态', default = 1)
	def __unicode__(self):
		return str(self.identification)
	class Meta:
		verbose_name = '订单信息'
		verbose_name_plural = '订单信息'

class OrderGoods(models.Model):
	identification = models.IntegerField('账号')
	phone = models.IntegerField('手机号')
	goods_name = models.CharField('商品名称', max_length = 20)
	money_need = models.CharField('所需金钱', max_length = 10)
	goods_number = models.IntegerField('商品数量', default = 1, null = True)
	def __unicode__(self):
		return self.goods_name
	class Meta:
		verbose_name = '订单商品信息'
		verbose_name_plural = '订单商品信息'

# Create your models here.
