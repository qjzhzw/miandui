from django.conf.urls import url

from . import views

urlpatterns=[
	url(r'^login/', views.login, name='login'),
	url(r'^vertification/', views.vertification, name='vertification'),
	url(r'^register/', views.register, name='register'),
	url(r'^forget_vertification/', views.forget_vertification, name='forget_vertification'),
	url(r'^forget_login/', views.forget_login, name='forget_login'),
	url(r'^information_get/', views.information_get, name='information_get'),
	url(r'^information_post/', views.information_post, name='information_post'),
	url(r'^timing_post/', views.timing_post, name='timing_post'),
	url(r'^mark_get_days/', views.mark_get_days, name='mark_get_days'),
	url(r'^mark_get_today/', views.mark_get_today, name='mark_get_today'),
	url(r'^shop_list_get/', views.shop_list_get, name='shop_list_get'),
	url(r'^goods_list_get/', views.goods_list_get, name='goods_list_get'),
	url(r'^goods_information_get/', views.goods_information_get, name='goods_information_get'),
	url(r'^discount_buy/', views.discount_buy, name='discount_buy'),
	url(r'^discount_list_get/', views.discount_list_get, name='discount_list_get'),
	url(r'^buy_list_get/', views.buy_list_get, name='buy_list_get'),
	url(r'^discount_use/', views.discount_use, name='discount_use'),
	url(r'^daily_sign_in/', views.daily_sign_in, name='daily_sign_in'),
	url(r'^friend_list_get/', views.friend_list_get, name='friend_list_get'),
	url(r'^friend_add_list_sender/', views.friend_add_list_sender, name='friend_add_list_sender'),
	url(r'^friend_add_list_receiver/', views.friend_add_list_receiver, name='friend_add_list_receiver'),
	url(r'^friend_add_request/', views.friend_add_request, name='friend_add_request'),
	url(r'^friend_add_response/', views.friend_add_response, name='friend_add_response'),
	url(r'^friend_rank_list_get/', views.friend_rank_list_get, name='friend_rank_list_get'),
	url(r'^advertisement_list_get/', views.advertisement_list_get, name='advertisement_list_get'),
	url(r'^prize_list_get/', views.prize_list_get, name='prize_list_get'),
	url(r'^prize_get/', views.prize_get, name='prize_get'),
	url(r'^prize_num_buy/', views.prize_num_buy, name='prize_num_buy'),
	url(r'^card_search/', views.card_search, name='card_search'),
	
	url(r'^APP_download/', views.APP_download, name='APP_download'),
	url(r'^version_update/', views.version_update, name='version_update'),

	url(r'^login_2/', views.login_2, name='login_2'),
	url(r'^register_2/', views.register_2, name='register_2'),
	url(r'^order_list_get_2/', views.order_list_get_2, name='order_list_get_2'),
]