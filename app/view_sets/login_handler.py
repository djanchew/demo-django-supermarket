from django.http import HttpResponse
from django.shortcuts import render, redirect

from ..models import Manager


def login(request):
    if request.method == 'POST':
        account = request.POST['account']
        pwd = request.POST['pwd']
        manager = Manager.objects.filter(account=account, pwd=pwd)
        if manager:
            request.session['is_login'] = '1'
            request.session['account_id'] = manager[0].id
            request.session.set_expiry(0)  # 关闭浏览器时删除会话
            return HttpResponse("ok")
        return HttpResponse("no")
    else:
        return render(request, 'manage/login.html')


def logout(request):
    request.session['is_login'] = '0'
    return redirect('/')
