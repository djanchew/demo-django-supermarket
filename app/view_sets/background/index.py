# 总览图表，近七天销售情况
from django.shortcuts import render

from ...libs.login_check import check_login
from ...models import Record, Goods


@check_login([0, 1, 2, 3])
def view_all(request, c, n_f, n_n):
    # 获取日期范围7天内的数据集合
    from datetime import datetime
    from datetime import timedelta
    from ...templatetags import my_tags
    today = datetime.now()
    date_list = []  # 日期列表
    sale_list = []  # 销售量列表
    price_list = []  # 销售额列表
    income_list = []  # 盈利列表
    sale_max = 0  # 最高销量

    loc_1 = []
    loc_2 = []
    loc_4 = []
    # from django.utils.safestring import mark_safe
    for i in range(0, 7).__reversed__():
        date = today - timedelta(days=i)
        if request.GET.get('loc'):
            loc = request.GET.get('loc')
            record = Record.objects.filter(date=date, sale_num__gt=0, location=loc)
        else:
            record = Record.objects.filter(date=date, sale_num__gt=0)  # 这是一整天的记录列表！！
        sale_num = my_tags.get_all_sale(record)  # 这是一整天的销售量，不分超市
        if record.count() > 0:
            if sale_num > sale_max:
                # sale_max = sale_num
                sale_max_name = record[0].goods.name  # 最高销量的商品名

            for r in record:
                if r.location == 1:
                    loc_1.append(r.sale_num)
                if r.location == 2:
                    loc_2.append(r.sale_num)
                if r.location == 4:
                    loc_4.append(r.sale_num)

                price = r.goods.sale_price - r.goods.lower  # 单价x数量
                income = price - r.goods.cost_price
                price_list.append(price * r.sale_num)
                income_list.append(income * r.sale_num)

        date_list.append(datetime.strftime(date, '%Y-%m-%d'))
        sale_list.append(sale_num)

    sale_sum = sum(sale_list)
    price_sum = '{:.2f}'.format(sum(price_list))
    income_sum = '{:.2f}'.format(sum(income_list))

    loc_1 = sum(loc_1)
    loc_2 = sum(loc_2)
    loc_4 = sum(loc_4)

    # 分别展示时候会有bug，0不能被除
    if loc_1 == 0:
        ploc_1 = '{:.2%}'.format(0)
    else:
        ploc_1 = '{:.2%}'.format(loc_1 / sale_sum)
    if loc_2 == 0:
        ploc_2 = '{:.2%}'.format(0)
    else:
        ploc_2 = '{:.2%}'.format(loc_2 / sale_sum)
    if loc_4 == 0:
        ploc_4 = '{:.2%}'.format(0)
    else:
        ploc_4 = '{:.2%}'.format(loc_4 / sale_sum)

    # 登陆后的第一个界面，在这里检测过期商品
    import datetime
    day = datetime.datetime.now() + datetime.timedelta(days=15)
    goods = Goods.objects.filter(limit_date__lt=day)

    return render(request, 'manage/dashboard.html', locals())
