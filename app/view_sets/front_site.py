from django.shortcuts import render

from ..libs.data_generator import *
from ..libs.page_generator import page_generator
from ..models import Message


def index(request):
    locals().update(get_hot(request))
    locals().update(get_new(request))
    locals().update(get_cheap(request))
    return render(request, 'home/index.html', locals())


def all(request):
    '''
    显示所有商品
        - get带参数sort时，返回相应的分类过滤结果
        - post带参数key时，模糊查询商品并返回结果
    :returns
        - sort: 前端显示分类信息
        - flag: 区分前端展示内容，以及分页器复用
        - key, value: 分页器中url的附加参数
    '''
    locals().update(get_hot(request))
    locals().update(get_new(request))
    locals().update(get_cheap(request))

    if request.GET.get('sort'):
        sort = request.GET.get('sort')
        good_list = Goods.objects.filter(sort=sort, isDelete=0)
        key = 'sort'
        value = request.GET.get('sort')
        flag = 1
    elif request.GET.get('Search'):
        from django.db.models import Q
        key = request.GET['Search']
        good_list = Goods.objects.filter(Q(name__icontains=key) & Q(isDelete=0))

        key = 'Search'
        value = request.GET.get('Search')
        flag = 0
    else:
        good_list = Goods.objects.filter(isDelete=0)
    len = good_list.count()
    locals().update(page_generator(request, good_list))
    return render(request, "home/all.html", locals())


def detail(request):
    id = request.GET['id']
    good = Goods.objects.filter(id=id, isDelete=0)[0]
    locals().update(get_new(request))
    return render(request, 'home/detail.html', locals())


def about(request):
    message = Message.objects.filter(type=1)
    return render(request, 'home/about.html', {'message': message})


def feedback(request):
    return render(request, 'home/feedback.html')
