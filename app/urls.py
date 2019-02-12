from django.urls import path
from django.views.generic.base import RedirectView

from .view_sets import front_site, message_handler, login_handler
from .view_sets.background import accounts, providers, goods, purchase, records, sales, index

urlpatterns = [
    path('favicon.ico', RedirectView.as_view(url='/static/hs.ico')),

    path('', front_site.index, name='index'),
    path('all/', front_site.all, name='goods_all'),
    path('detail/', front_site.detail, name='goods_detail'),
    path('about/', front_site.about, name='about'),
    path('feedback/', front_site.feedback, name='feedback'),
    path('send_feedback/', message_handler.send_feedback, name='send_feedback'),

    path('login/', login_handler.login, name='login'),
    path('logout/', login_handler.logout, name='logout'),

    # 账号管理
    path('account_all/', accounts.account_all, name='account_all'),
    path('account_add/', accounts.account_add, name='account_add'),
    path('account_exist/', accounts.account_exist, name='account_exist'),
    path('account_update/', accounts.account_update, name='account_update'),
    path('account_delete/', accounts.account_delete, name='account_delete'),
    path('profile/', accounts.profile, name='profile'),
    # 供应商管理
    path('provider/', providers.provider_all, name='providers'),
    path('provider_add/', providers.provider_add, name='provider_add'),
    path('provider_delete/', providers.provider_delete, name='provider_delete'),
    path('provider_update/', providers.provider_update, name='provider_update'),
    # 商品管理
    path('goods/', goods.goods_all, name='goods_manage'),
    path('good_lower/', goods.good_lower, name='good_lower'),
    path('good_edit/', goods.good_edit, name='good_edit'),
    path('limit/', goods.goods_all, name='limit'),
    path('good_remove/', goods.good_remove, name='good_remove'),
    # 进货管理
    path('purchase/', purchase.purchase, name='purchase'),
    path('purchase_supplement/', purchase.purchase_supplement, name='purchase_supplement'),
    # 记录查询
    path('records/', records.records, name='records'),
    path('storage/', records.storage, name='storage'),

    path('messages/', message_handler.show_messages, name='messages'),
    path('new_messages/', message_handler.new_messages, name='new_messages'),
    path('new_notifications/', message_handler.new_messages, name='new_notifications'),
    path('is_read/', message_handler.new_messages, name='is_read'),
    path('send_note/', message_handler.send_note, name='send_note'),
    # 销售台
    path('sale/', sales.sale, name='sale'),
    path('sale_record/', sales.sale_record, name='sale_record'),
    # 销售概况
    path('view_all/', index.view_all, name='view_all'),

]
