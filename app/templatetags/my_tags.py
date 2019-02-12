from django import template

register = template.Library()


@register.filter(name='get_simple_operation_num')
def get_simple_operation_num(obj):
    if obj.purchase_num:
        return obj.purchase_num
    if obj.sale_num:
        return obj.sale_num
    if obj.withdraw_num:
        return obj.withdraw_num


@register.filter(name='get_simple_operation')
def get_simple_operation(obj):
    if obj.purchase_num:
        return '进货'
    if obj.sale_num:
        return '出售'
    if obj.withdraw_num:
        return '退货'


@register.filter(name='get_sub_date')
def get_sub_date(date):
    import datetime
    today = datetime.datetime.now().date()
    if (today - date).days == 0:
        return '今天'
    return str((today - date).days) + '天前'


@register.filter(name='get_right_top')
def get_right_top(obj):  # 返回对应的右上角图片名字
    if obj.lower > 0:
        return 'cheap'

    import datetime
    today = datetime.datetime.now().date()
    q_set = obj.record_set.filter(purchase_num__gt=0)
    for q in q_set:
        r_day = q.date
        print(today - r_day)
        print((today - r_day).days)
        if (today - r_day).days <= 7:
            return 'offer'

    record_set = obj.record_set.filter(sale_num__isnull=False)
    if get_all_sale(record_set) > 70:
        return 'hot'

    else:
        return 'blank'


@register.simple_tag(name='get_cheap_price')
def get_cheap_price(sale_price, lower):
    return round(sale_price - lower, 2)  # 返回两位小数的浮点数


@register.filter(name='get_simple_sort')
def get_simple_sort(sort):
    if sort:
        if int(sort) == 0:
            return '零食饮料'
        elif int(sort) == 1:
            return '生鲜果蔬'
        elif int(sort) == 2:
            return '粮油副食'
        elif int(sort) == 3:
            return '清洁用品'
        elif int(sort) == 4:
            return '家居家电'
        elif int(sort) == 5:
            return '全部商品'
        elif int(sort) == 6:
            return '搜索'
    else:
        return "None"


@register.filter(name='get_simple_location')
def get_simple_location(loc):
    if loc == 1:
        return '一饭'
    elif loc == 2:
        return '三饭'
    elif loc == 4:
        return '东区'


# @register.simple_tag()
@register.simple_tag(name='record_get_location')
# multiple
def record_get_location(record_set, flag=0):  # 这里的flag是用来区分这个方法是在前台还是后台，1为前台
    # set()不支持取值，先用list存好，然后set(list)转换，然后再转换回list，完成去重
    location_list = [0]
    for i in record_set:
        location_list.append(i.location)

    loc = set(location_list)
    location_list = list(loc)
    # print(location_list)
    l = sum(location_list)
    if l == 1:
        return "一饭"
    elif l == 2:
        return "三饭"
    elif l == 3:
        return "一饭/三饭"
    elif l == 4:
        return "东区"
    elif l == 5:
        return "一饭/东区"
    elif l == 6:
        return "三饭/东区"
    elif l == 7:
        return "一饭/三饭/东区"
    else:
        if flag == 1:
            return "抱歉！该商品暂时无货，我们会在三个工作日内进货，给您带来不便敬请谅解！"
        else:
            return "无货"


@register.filter(name='record_get_storage')
def record_get_storage(record_set):
    sale_list = [0]
    purchase_list = [0]
    for i in record_set:
        # 如果有出售记录。
        if i.sale_num:
            sale_list.append(i.sale_num)
        if i.purchase_num:
            purchase_list.append(i.purchase_num)
    s = sum(sale_list)
    p = sum(purchase_list)
    return p - s


@register.simple_tag(name='get_storage_by_loc')
def get_storage_by_loc(record_set, loc):
    sale_list = [0]
    purchase_list = [0]
    for i in record_set:
        # 如果有出售记录。
        if i.location == loc:
            if i.sale_num:
                sale_list.append(i.sale_num)
            if i.purchase_num:
                purchase_list.append(i.purchase_num)
    s = sum(sale_list)
    p = sum(purchase_list)
    return p - s


@register.filter(name='get_all_sale')
def get_all_sale(record_set):  # 传入记录对象列表
    sale_list = [0]  # 出售记录列表，保存出售数量
    for i in record_set:
        if i.sale_num:  # 如果有出售记录
            sale_list.append(i.sale_num)  # 如果有销售记录，增加到sale_list
    s = sum(sale_list)  # 求总销量
    return s


@register.simple_tag(name='get_limit_period')
def get_limit_period(produce, limit):
    import datetime
    days = (limit - datetime.datetime.now().date()).days

    if days < 0:
        return str(days) + '天' + '\n已过期'
    elif days < 31 and days > 0:
        return str(days) + '天'
    elif days > 31 and days < 365:
        return str(days // 31) + '个月' + str(days % 31) + '天'
    elif days > 365:
        return str(days // 365) + '年' + str((days % 365) // 31) + '个月' + str(days % 31) + '天'


@register.simple_tag(name='get_object_id')
def get_object_id(dict, key):
    return dict.get(key).id


@register.simple_tag(name='get_object_name')
def get_object_name(dict, key):
    return dict.get(key).name


@register.simple_tag(name='get_object_sale_price')
def get_object_sale_price(dict, key):
    return dict.get(key).sale_price


@register.simple_tag(name='get_object_purchase_price')
def get_object_purchase_price(dict, key):
    return dict.get(key).purchase_price


@register.simple_tag(name='get_object_img')
def get_object_img(dict, key):
    return str(dict.get(key).sort) + '_' + str(dict.get(key).id)


@register.filter(name='get_authority')
def get_authority(obj):
    if obj.authority == 0:
        return "超级管理员"
    elif obj.authority == 1:
        return "经理"
    elif obj.authority == 2:
        return "采购员"
    elif obj.authority == 3:
        return "销售员"
    else:
        return "unknown"


@register.simple_tag(name='get_gender')
def get_gender(obj, polite):
    if obj.gender == 0:
        if polite == 1:
            return "女士"
        else:
            return "女"
    elif obj.gender == 1:
        if polite == 1:
            return "先生"
        else:
            return "男"
    else:
        return "unknown"
