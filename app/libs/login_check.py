from functools import wraps
from django.shortcuts import render, redirect

from ..models import Manager, Message


def check_login(group):
    '''
    检查登录状态
    - 接收一个整数列表group
        - 包含0123 (分别代表超级管理员，经理，采购员，销售员)，以此赋予方法的使用权限，
        - 当权限不足时返回提示信息
    - 被装饰的方法会接收到额外的参数：当前登录的对象，新反馈条数，新通知条数
    '''

    def decorator(func):
        @wraps(func)
        def inner(request, *arg, **kwargs):
            if request.session.get('is_login') == '1':
                id = request.session.get('account_id')
                current_account = Manager.objects.filter(id=id)[0]
                if current_account.authority not in group:
                    return render(request, '404.html')
                new_feedback = Message.objects.filter(type=1, isRead=0).count()
                new_notifications = Message.objects.filter(type=0, isRead=0).count()
                return func(request, current_account, new_feedback, new_notifications, *arg, **kwargs)
            else:
                return redirect('/login')

        return inner

    return decorator
