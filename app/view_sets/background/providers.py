from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from ...libs.login_check import check_login
from ...models import Provider, Goods


@check_login([0, 1, 2, 3])
def provider_all(request, c, n_f, n_n):
    provider = Provider.objects.all()
    goods = Goods.objects.filter(isDelete=0)
    return render(request, 'manage/provider.html', locals())


# 添加供应商
@check_login([0, 1, 2])
@csrf_exempt
def provider_add(request, c, n_f, n_n):
    Provider.objects.create(
        name=request.POST['name'],
        address=request.POST['address'],
        phone=request.POST['phone'],
    )
    return HttpResponse('ok')


# 修改供应商
@check_login([0, 1, 2])
@csrf_exempt
def provider_update(request, c, n_f, n_n):
    Provider.objects.filter(id=request.POST['id']).update(
        name=request.POST['name'],
        address=request.POST['address'],
        phone=request.POST['phone'],
    )
    return HttpResponse('ok')


@check_login([0, 1, 2])
def provider_delete(request, c, n_f, n_n):
    Provider.objects.filter(id=request.GET['id']).delete()
    return redirect('/provider')