# 出售
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from ...libs.login_check import check_login
from ...models import Record, Goods


@check_login([0, 1, 2, 3])
@csrf_exempt
def sale(request, c, n_f, n_n):
    if request.method == "POST":
        from django.core import serializers
        key = request.POST.get('key')

        # 先做判断，如果有库存则返回一个good对象
        from ...templatetags import my_tags
        loc = int(request.POST['loc'])
        record_set = Record.objects.filter(goods_id=key, location=loc)
        storage = my_tags.record_get_storage(record_set)
        if storage <= 0:
            return HttpResponse('无货')
        else:
            result = Goods.objects.filter(id=key, isDelete=0)
            data = serializers.serialize('json', result)
            final = data[:-1] + ', {"storage": ' + str(storage) + '}]'  # 添加额外字段，构造js可识别的json，格式
            return HttpResponse(final)
    elif request.GET.get('loc'):
        loc = int(request.GET['loc'])
        return render(request, 'manage/sale.html', locals())
    else:
        return HttpResponse('404')


# 添加出售记录
@check_login([0, 1, 2, 3])
@csrf_exempt
def sale_record(request, c, n_f, n_n):
    concat = request.POST  # QueryDict对象
    print(concat)
    j = 1
    for i in concat:  # 有很多个字段岂不是要循环好多次？
        if j == 1:
            loc = concat[i]
        if j == 2:
            goods_id = concat[i]
        if j == 3:
            sale_num = concat[i]
            Record.objects.create(goods_id=goods_id, location=loc, sale_num=sale_num)
            j = 0
        j += 1
    return HttpResponse('ok')