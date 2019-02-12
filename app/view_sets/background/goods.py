from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from ...libs.login_check import check_login
from ...libs.page_generator import page_generator
from ...models import Goods, Record, Provider


@check_login([0, 1, 2])
def goods_all(request, c, n_f, n_n):
    if request.path == "/limit/":  # 临近期限的商品或者过期的商品
        import datetime
        day = datetime.datetime.now() + datetime.timedelta(days=15)
        goods = Goods.objects.filter(limit_date__lt=day)
        is_limit = 1
    elif request.GET.get('Search'):  # 商品搜索post
        from django.db.models import Q
        key = 'Search'
        value = request.GET['Search']
        flag = 1
        goods = Goods.objects.filter(Q(name__icontains=value) & Q(isDelete=0) | Q(id__icontains=value) & Q(
            isDelete=0))  # | Q(id__icontains=key)
    elif request.GET.get('p_id'):  # 供应商传过来的，查看指定供应商的商品
        goods = Goods.objects.filter(provider_id=request.GET['p_id'], isDelete=0)
        key = 'pid'
        value = request.GET.get('p_id')
        flag = 1
    elif request.GET.get('g_id'):  # 竟然忘记这个干嘛用的。难道是一开是用g_id查商品？留着吧
        goods = Goods.objects.filter(id=request.GET['g_id'], isDelete=0)
        flag = 0
    elif request.GET.get('loc'):
        loc = int(request.GET['loc'])
        record_set = Record.objects.filter(location=loc)
        goods = []
        for r in list(record_set):
            if r.purchase_num != None and r.sale_num == None:
                storage = r.purchase_num
            elif r.purchase_num != None and r.sale_num != None:
                storage = r.purchase_num - r.sale_num
            else:
                storage = 0
            if storage > 0:
                try:
                    goods.append(Goods.objects.filter(id=r.goods.id, isDelete=0)[0])
                except Exception as e:
                    pass
        flag = 1
        key = 'loc'
        value = loc
    else:
        goods = Goods.objects.filter(isDelete=0)
    len = goods.__len__()
    locals().update(page_generator(request, goods))
    return render(request, 'manage/goods.html', locals())


# 添加降价数据
@check_login([0, 1])
@csrf_exempt
def good_lower(request, c, n_f, n_n):
    id = request.POST['id']
    lower = request.POST['lower']
    g = Goods.objects.filter(id=id, isDelete=0)
    if float(lower) > g[0].sale_price - g[0].cost_price:
        return HttpResponse('低于成本价')
    else:
        g.update(lower=lower)
        return HttpResponse('ok')


# 商品修改，get商品id，转到填好信息的商品修改页（进货页改）
@check_login([0, 1, 2])
@csrf_exempt
def good_edit(request, c, n_f, n_n):
    if request.method == "GET":
        id = request.GET['id']
        eg = Goods.objects.filter(isDelete=0, id=id)[0]
        p = Provider.objects.all()
        is_edit = 1
        return render(request, 'manage/purchase.html', locals())
    elif request.method == 'POST':
        from django.conf import settings
        import datetime
        produce_date = datetime.datetime.strptime(str(request.POST['good_produce_date']), '%Y-%m-%d').date(),
        limit_date = datetime.datetime.strptime(str(request.POST['good_limit_date']), '%Y-%m-%d').date(),
        if limit_date > produce_date:
            Goods.objects.filter(id=request.POST['id']).update(
                name=request.POST['good_name'],
                sort=int(request.POST['good_sort']),
                cost_price=float(request.POST['good_cost_price']),
                sale_price=float(request.POST['good_sale_price']),
                produce_date=datetime.datetime.strptime(str(request.POST['good_produce_date']), '%Y-%m-%d').date(),
                limit_date=datetime.datetime.strptime(str(request.POST['good_limit_date']), '%Y-%m-%d').date(),
                weight=float(request.POST['good_weight']),
                provider_id=int(request.POST['good_provider']),
            )
        else:
            return HttpResponse('过期时间早于生产时间')
        if request.FILES.get('good_image'):
            f1 = request.FILES['good_image']
            fname = '%s/goods_img/%s' % (
                settings.MEDIA_ROOT, request.POST['good_sort'] + '_' + str(request.POST['id']) + '.png')
            with open(fname, 'wb') as pic:
                for c in f1.chunks():
                    pic.write(c)
        return HttpResponse('ok')
    else:
        return HttpResponse('404')


# 商品下架/删除（逻辑）
@check_login([0, 1])
@csrf_exempt
def good_remove(request, c, n_f, n_n):
    Goods.objects.filter(id=request.POST['id']).update(isDelete=1)
    return HttpResponse("ok")