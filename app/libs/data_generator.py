from ..models import Goods, Record
from ..templatetags import my_tags


# 获取热卖商品(前6个)
def get_hot(request):
    goods = Goods.objects.filter(isDelete=0)
    dict = {}  # key：总销量，value：单条数据对象
    for g in goods:
        record_set = g.record_set.filter(sale_num__isnull=False)  # 过滤出sale记录的对象集合
        if record_set:
            dict[my_tags.get_all_sale(record_set)] = g
    hot_keys = sorted(dict.keys(), reverse=True)[:6]  # 将字典key(总销量)降序排序并切片，前闭后开，取前6个
    return locals()


# 获取新进商品(随机4个)
def get_new(request):
    record_set = Record.objects.filter(purchase_num__gt=0)  # 过滤出purchase记录的对象集合
    import datetime
    today = datetime.datetime.now().date()
    new_list = []
    for r in record_set:
        if (today - r.date).days < 7:
            new_list.append(r)
    import random
    random.shuffle(new_list)
    new_list = new_list[:4]
    return locals()


# 获取降价商品，随机6个
def get_cheap(request):
    cheap_list = Goods.objects.filter(lower__gt=0, isDelete=0)
    import random
    cheap_list = list(cheap_list)
    random.shuffle(cheap_list)
    cheap_list = cheap_list[:6]
    return locals()
