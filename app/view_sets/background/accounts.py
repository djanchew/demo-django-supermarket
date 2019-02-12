from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from ...libs.login_check import check_login
from ...models import Manager


@check_login([0, 1])
def account_all(request, c, n_f, n_n):
    list = Manager.objects.all()
    count = [0, 1, 2, 3]
    return render(request, 'manage/account_all.html', locals())


@check_login([0])
@csrf_exempt
def account_add(request, c, n_f, n_n):
    if request.method == 'POST':
        account = request.POST['account']
        manager = Manager.objects.filter(account=account)
        if manager:
            return HttpResponse("账号已存在")
        else:
            Manager.objects.create(account=account, name=request.POST['name'], pwd=request.POST['pwd'],
                                   gender=int(request.POST['gender']), phone=request.POST['phone'],
                                   authority=int(request.POST['authority']))
            return HttpResponse('ok')
    else:
        return render(request, 'manage/account_more.html', {'name': c})


# ajax检查账号是否存在 输入框失去焦点触发
@check_login([0])
@csrf_exempt
def account_exist(request):
    manager = Manager.objects.filter(account=request.POST["account"])
    if manager:
        return HttpResponse("账号已存在")
    else:
        return HttpResponse('ok')


# 修改账号
@check_login([0])
@csrf_exempt  # 取消csrf验证
def account_update(request, c, n_f, n_n):
    if request.method == 'POST':
        Manager.objects.filter(
            id=request.POST['id']
        ).update(name=request.POST['name'], pwd=request.POST['pwd'],
                 gender=int(request.POST['gender']),
                 phone=request.POST['phone'],
                 authority=int(request.POST['authority']))
        return HttpResponse("ok")
    id = request.GET['id']
    info = Manager.objects.filter(id=id)[0]
    return render(request, 'manage/account_more.html', locals())


# 删除账号（逻辑，后觉得没必要，改回去）
@check_login([0])
def account_delete(request, c, n_f, n_n):
    id = request.GET['id']
    Manager.objects.filter(id=id).delete()
    return redirect('/account_all')


# 账号信息
@check_login([0, 1, 2, 3])
def profile(request, c, n_f, n_n):
    return render(request, 'manage/profile.html', locals())
