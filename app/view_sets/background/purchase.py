from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from ...libs.login_check import check_login
from ...models import Goods, Provider, Record

# 新进货/补库存
# 增加进货记录的同时，还要添加商品信息
@check_login([0, 1, 2])
@csrf_exempt
def purchase(request, c, n_f, n_n):
    # 新进货提交post
    if request.method == 'POST':
        from django.conf import settings
        import datetime
        if request.POST.get('good_name') and request.FILES['good_image']:
            # 如果post有名字，# 这里有bug，如果有数据没图片，会先保存一次数据，再报错
            produce_date = datetime.datetime.strptime(str(request.POST['good_produce_date']), '%Y-%m-%d').date(),
            limit_date = datetime.datetime.strptime(str(request.POST['good_limit_date']), '%Y-%m-%d').date(),
            if limit_date > produce_date:
                Goods.objects.create(
                    name=request.POST['good_name'],
                    sort=int(request.POST['good_sort']),
                    cost_price=float(request.POST['good_cost_price']),
                    sale_price=float(request.POST['good_sale_price']),
                    produce_date=datetime.datetime.strptime(str(request.POST['good_produce_date']),
                                                            '%Y-%m-%d').date(),
                    limit_date=datetime.datetime.strptime(str(request.POST['good_limit_date']), '%Y-%m-%d').date(),
                    weight=float(request.POST['good_weight']),
                    provider_id=int(request.POST['good_provider']),
                )
                goods_id = Goods.objects.filter(name=request.POST['good_name'], isDelete=0)[0].id
                Record.objects.create(
                    location=int(request.POST['good_location']),
                    purchase_num=int(request.POST['good_num']) * int(request.POST['good_piece']),
                    goods_id=goods_id,
                )
                f1 = request.FILES['good_image']
                fname = '%s/goods_img/%s' % (
                    settings.MEDIA_ROOT, request.POST['good_sort'] + '_' + str(goods_id) + '.png')
                with open(fname, 'wb') as pic:
                    for c in f1.chunks():
                        pic.write(c)
                return HttpResponse('ok')
            else:
                return HttpResponse('过期时间早于生产时间')
        else:
            return HttpResponse('No data detected')
    # 补货的get请求，传递商品信息
    if request.GET.get('id'):
        g_id = request.GET['id']
        if g_id != "null":
            good = Goods.objects.filter(id=g_id, isDelete=0)[0]
            is_supplement = 1
        is_supplement = 1
    providers = Provider.objects.all()
    goods = Goods.objects.filter(isDelete=0)
    return render(request, 'manage/purchase.html', locals())


# 补货
@check_login([0, 1, 2])
@csrf_exempt
def purchase_supplement(request, c, n_f, n_n):
    Record.objects.create(
        goods_id=request.POST['id'],
        location=request.POST['location'],
        purchase_num=request.POST['purchase_num'],
    )
    return HttpResponse("ok")
