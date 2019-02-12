from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def page_generator(request, list):
    '''
    分页器
    - 接收一个<Query Set>对象(或者多个对象形成的列表)，按照指定条数分页。
    - 这里统一设置为9
    '''
    paginator = Paginator(list, 9)
    page = request.GET.get('page', 1)
    current_page = int(page)
    try:
        page_list = paginator.page(page)  # 获取当前页码的记录
    except PageNotAnInteger:
        page_list = paginator.page(1)  # 如果用户输入的页码不是整数时,显示第1页的内容
    except EmptyPage:
        page_list = paginator.page(paginator.num_pages)  # 如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容
    return locals()
