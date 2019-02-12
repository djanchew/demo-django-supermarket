from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt

from ..libs.login_check import check_login
from ..models import Message


def send_feedback(request):
    Message.objects.create(name=request.POST['Name'], content=request.POST['Message'], contact=request.POST['Contact'],
                           type=1)
    return redirect('/about')


@check_login([0])
def send_note(request, c, n_f, n_n):
    if request.method == 'POST':
        Message.objects.create(name=request.POST['Name'], content=request.POST['Message'],
                               contact=request.POST['Contact'],
                               type=0)
        return redirect('/view_all')
    else:
        return render(request, 'manage/send_note.html', locals())


@check_login([0, 1])
@csrf_exempt
def show_messages(request, c, n_f, n_n):  # 本来把所有的message的方法都定义在这里，可是出现了bug，即识别进去if了，又执行了else的东西？？？
    if request.POST.get('m_id'):  # 删除反馈
        Message.objects.filter(id=request.POST['m_id']).delete()
        return HttpResponse('ok')

    messages = Message.objects.filter(type=1)
    len = messages.count()
    return render(request, 'manage/messages.html', locals())


@check_login([0, 1])
@csrf_exempt
def new_messages(request, c, n_f, n_n):
    # 已读
    if request.method == 'POST':
        Message.objects.filter(id=request.POST['m_id']).update(isRead=1)
        return HttpResponse('ok')

    if request.path == "/new_messages/":  # 新反馈
        messages = Message.objects.filter(type=1, isRead=0)
        is_new = 1
    if request.path == "/new_notifications/":  # 系统通知
        messages = Message.objects.filter(type=0, isRead=0)
        is_new = 1
    return render(request, 'manage/messages.html', locals())
