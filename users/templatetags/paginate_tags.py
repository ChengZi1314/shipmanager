from django import template
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

register = template.Library()  # 这是定义模板标签要用到的


@register.simple_tag(takes_context=True)
def paginate(context, object_list, page_count):
    left = 3  # 当前页码左边显示几个页码号 -1，比如3就显示2个
    right = 3

    paginator = Paginator(object_list, page_count)
    page = context['request'].GET.get('page')

    try:
        object_list = paginator.page(page)  # 根据页码号获取第几页的数据
        context['current_page'] = int(page)  # 把当前页封装进context（上下文）中
        pages = get_left(context['current_page'], left, paginator.num_pages) \
                + get_right(context['current_page'], right, paginator.num_pages)
    except PageNotAnInteger:
        # 异常处理，如果用户传递的page值不是整数，则把第一页的值返回给他
        object_list = paginator.page(1)
        context['current_page'] = 1
        pages = get_right(context['current_page'], right, paginator.num_pages)
    except EmptyPage:
        # 如果用户传递的 page 值是一个空值，那么把最后一页的值返回给他
        object_list = paginator.page(paginator.num_pages)
        context['current_page'] = paginator.num_pages
        pages = get_left(context['current_page'], left, paginator.num_pages)

    context['crew_list'] = object_list
    context['cv_list'] = object_list
    context['post_list'] = object_list
    context['article_list'] = object_list
    context['recruit_list'] = object_list
    context['user_list'] = object_list  # 把获取到的分页的数据封装到上下文中
    context['pages'] = pages  # 把页码号列表封装进去
    context['last_page'] = paginator.num_pages   # 最后一页的页码号
    context['first_page'] = 1   # 第一页的页码号为1
    try:
        # 获取 pages 列表第一个值和最后一个值，主要用于在是否该插入省略号的判断，
        # 在模板文件中将会体会到它的用处。
        context['pages_first'] = pages[0]
        context['pages_last'] = pages[-1] + 1
        # +1的原因是为了方便判断，在模板文件中将会体会到其作用。
    except IndexError:
        context['pages_first'] = 1  # 发生异常说明只有1页
        context['pages_last'] = 2   # 1 + 1 后的值

    return ''  # 必须加这个，否则首页会显示个None


def get_left(current_page, left, num_pages):
    # 辅助函数，获取当前页码的值的左边两个页码值，要注意一些细节，比如不够两个
    # 那么最左取到2，为了方便处理，包含当前页码值，比如当前页码值为5，
    # 那么pages = [3,4,5]
    if current_page == 1:
        return []
    elif current_page == num_pages:
        l = [i - 1 for i in range(current_page, current_page - left, -1)
             if i - 1 > 1]
        l.sort()  # python 中的sort函数是内部函数，将l原地排序
        return l
    l = [i for i in range(current_page, current_page - left, -1) if i > 1]
    l.sort()
    return l


def get_right(current_page, right, num_pages):
    # 辅助函数，获取当前页码的值得右边两个页码值，要注意一些细节，
    # 比如不够两个那么最右取到最大页码值。不包含当前页码值。比如当前页码值为5，
    # 那么pages = [6,7]
    if current_page == num_pages:
        return []
    return [i + 1 for i in range(current_page, current_page + right - 1)
            if i < num_pages - 1]
