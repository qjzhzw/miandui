from django.contrib import admin

from .models import User, Phone, Timing, Shop, Goods, Discount, Friend, Advertisement, Prize, Order, OrderGoods

class UserAdmin(admin.ModelAdmin):
	list_display = ('identification', 'nickname', 'mark', 'time_login')
	fieldsets = (
		['基本信息',{
			'fields':('identification', 'password'),
		}],
		['个人信息',{
			'fields': ('nickname', 'sex', 'birthday', 'motto', 'head'),
		}],
		['计时信息',{
			'fields': ('mark', 'timing_useful'),
		}],
		['时间信息',{
			'fields': ('time_register', 'time_login'),
		}],
		['签到信息',{
			'fields': ('date_sign_in', 'day_sign_in', 'mark_sign_in'),
		}],
		['抽奖信息',{
			'fields': ('num_prize',),
		}],
	)
	search_fields = ('identification',)
	
class PhoneAdmin(admin.ModelAdmin):
	list_display = ('identification', 'code', 'code_start', 'code_end')
	fieldsets = (
		['验证码',{
			'fields': ('identification', 'code', 'code_start', 'code_end'),
		}],
	)
	
class TimingAdmin(admin.ModelAdmin):
	list_display = ('identification', 'date', 'time_start', 'time_end', 'timing_useful', 'mark', 'number')
	fieldsets = (
		['计时有效时间',{
			'fields': ('identification', 'date', 'time_start', 'time_end', 'timing_useful', 'mark', 'number'),
		}],
	)
	list_filter = ('identification', 'date')
	
class ShopAdmin(admin.ModelAdmin):
	list_display = ('identification', 'shop_name', 'shop_address', 'shop_telephone', 'time_register')
	fieldsets = (
		['基本信息',{
			'fields':('identification', 'password'),
		}],
		['商店信息',{
			'fields': ('shop_id', 'shop_name', 'shop_address', 'shop_telephone', 'shop_image', 'time_register'),
		}],
	)
	search_fields = ('shop_name',)
	
class GoodsAdmin(admin.ModelAdmin):
	list_display = ('goods_id', 'shop_name', 'goods_name', 'mark_need', 'money_need')
	fieldsets = (
		['商品信息',{
			'fields': ('goods_id', 'shop_name', 'goods_name', 'goods_information', 'goods_introduction', 'goods_image', 'goods_number'),
		}],
		['购买信息',{
			'fields': ('mark_need', 'money_need', 'money_origin'),
		}],
	)
	list_filter = ('shop_name',)
	search_fields = ('goods_name',)
	
class DiscountAdmin(admin.ModelAdmin):
	list_display = ('identification', 'goods_id', 'shop_name', 'goods_name', 'mark_need', 'money_need', 'status', 'time_use')
	fieldsets = (
		['商品信息',{
			'fields': ('goods_id', 'shop_name', 'goods_name', 'goods_information', 'goods_introduction', 'goods_image'),
		}],
		['购买信息',{
			'fields': ('identification', 'mark_need', 'money_need', 'money_origin', 'status'),
		}],
		['时间信息',{
			'fields': ('time_buy', 'time_use'),
		}],
	)
	list_filter = ('identification', 'goods_id')
	search_fields = ('goods_name',)
	
class FriendAdmin(admin.ModelAdmin):
	list_display = ('identification_sender', 'identification_receiver', 'status')
	fieldsets = (
		['好友双方信息',{
			'fields': ('identification_sender', 'identification_receiver', 'status'),
		}],
		['时间信息',{
			'fields': ('time_request', 'time_response'),
		}],
	)
	list_filter = ('identification_sender', 'identification_receiver', 'status')
	search_fields = ('identification_sender', 'identification_receiver')
	
class AdvertisementAdmin(admin.ModelAdmin):
	list_display = ('words', 'image')
	fieldsets = (
		['广告信息',{
			'fields': ('words', 'image'),
		}],
	)
	search_fields = ('words',)
	
class PrizeAdmin(admin.ModelAdmin):
	list_display = ('words',)
	fieldsets = (
		['抽奖信息',{
			'fields': ('words',),
		}],
	)
	search_fields = ('words',)

class OrderAdmin(admin.ModelAdmin):
	list_display = ('identification', 'phone', 'time_arrive', 'status')
	fieldsets = (
		['订单信息',{
			'fields': ('identification', 'phone', 'time_arrive', 'money_discount', 'money_service', 'status'),
		}],
	)
	search_fields = ('identification',)

class OrderGoodsAdmin(admin.ModelAdmin):
	list_display = ('identification', 'phone', 'goods_name', 'money_need', 'goods_number')
	fieldsets = (
		['订单商品信息',{
			'fields': ('identification', 'phone', 'goods_name', 'money_need', 'goods_number'),
		}],
	)
	search_fields = ('goods_name',)

admin.site.register(User, UserAdmin)
admin.site.register(Phone, PhoneAdmin)
admin.site.register(Timing, TimingAdmin)
admin.site.register(Shop, ShopAdmin)
admin.site.register(Goods, GoodsAdmin)
admin.site.register(Discount, DiscountAdmin)
admin.site.register(Friend, FriendAdmin)
admin.site.register(Advertisement, AdvertisementAdmin)
admin.site.register(Prize, PrizeAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderGoods, OrderGoodsAdmin)

# Register your models here.