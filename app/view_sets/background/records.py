# 记录查询
from django.shortcuts import render

from ...libs.login_check import check_login
from ...libs.page_generator import page_generator
from ...models import Record, Goods


@check_login([0, 1])
def records(request, c, n_f, n_n):
    records = Record.objects.all()
    len = records.count()
    flag = 0  # 不是传递provider的参数的get
    locals().update(page_generator(request, records))
    return render(request, 'manage/record.html', locals())


# 库存查询，从商品管理copy的
@check_login([0, 1, 2])
def storage(request, c, n_f, n_n):
    if request.method == 'POST':
        from django.db.models import Q
        key = request.POST['Search']
        goods = Goods.objects.filter(Q(name__icontains=key) & Q(isDelete=0))
    elif request.GET.get('g_id'):
        goods = Goods.objects.filter(id=request.GET['g_id'], isDelete=0)
        flag = 0
    else:
        goods = Goods.objects.filter(isDelete=0)
    len = goods.count()
    locals().update(page_generator(request, goods))
    return render(request, 'manage/storage.html', locals())