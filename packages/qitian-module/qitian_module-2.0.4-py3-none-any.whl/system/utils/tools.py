from django.http import QueryDict
from urllib.parse import urlencode, urlparse
import time
import datetime
import re
from bs4 import BeautifulSoup
import requests
from system.models import BaiduPushLog


def pagination_tool(context, request):
    """
    分页模板见 usercenter/templates/part/pagination.html
    :param context:
    :param request:
    :return:
    """
    paginator = context.get('paginator')
    page = context.get('page_obj')
    is_paginated = context.get('is_paginated')
    if not is_paginated:
        # 如果没有分页，则无需显示分页导航条，不用任何分页导航条的数据，因此返回一个空的字典
        return {}

    url_info = urlparse(request.get_raw_uri())
    params = QueryDict(url_info.query)
    query_dict = {}
    for key in params:
        if key == 'page':
            continue
        query_dict[key] = params.get(key)
    query_str = urlencode(query_dict)

    list_num = 5
    # 当前页左边连续的页码号，初始值为空
    left = []

    # 当前页右边连续的页码号，初始值为空
    right = []

    # 标示第 1 页页码后是否需要显示省略号
    left_has_more = False

    # 标示最后一页页码前是否需要显示省略号
    right_has_more = False

    # 标示是否需要显示第 1 页的页码号。
    # 因为如果当前页左边的连续页码号中已经含有第 1 页的页码号，此时就无需再显示第 1 页的页码号，
    # 其它情况下第一页的页码是始终需要显示的。
    # 初始值为 False
    first = False

    # 标示是否需要显示最后一页的页码号。
    # 需要此指示变量的理由和上面相同。
    last = False

    # 获得用户当前请求的页码号
    page_number = page.number

    # 获得分页后的总页数
    total_pages = paginator.num_pages

    # 获得整个分页页码列表，比如分了四页，那么就是 [1, 2, 3, 4]
    page_range = paginator.page_range

    if page_number == 1:
        # 如果用户请求的是第一页的数据，那么当前页左边的不需要数据，因此 left=[]（已默认为空）。
        # 此时只要获取当前页右边的连续页码号，
        # 比如分页页码列表是 [1, 2, 3, 4]，那么获取的就是 right = [2, 3]。
        # 注意这里只获取了当前页码后连续两个页码，你可以更改这个数字以获取更多页码。
        right = page_range[page_number:page_number + list_num]

        # 如果最右边的页码号比最后一页的页码号减去 1 还要小，
        # 说明最右边的页码号和最后一页的页码号之间还有其它页码，因此需要显示省略号，通过 right_has_more 来指示。
        if right[-1] < total_pages - 1:
            right_has_more = True

        # 如果最右边的页码号比最后一页的页码号小，说明当前页右边的连续页码号中不包含最后一页的页码
        # 所以需要显示最后一页的页码号，通过 last 来指示
        if right[-1] < total_pages:
            last = True

    elif page_number == total_pages:
        # 如果用户请求的是最后一页的数据，那么当前页右边就不需要数据，因此 right=[]（已默认为空），
        # 此时只要获取当前页左边的连续页码号。
        # 比如分页页码列表是 [1, 2, 3, 4]，那么获取的就是 left = [2, 3]
        # 这里只获取了当前页码后连续两个页码，你可以更改这个数字以获取更多页码。
        left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]

        # 如果最左边的页码号比第 2 页页码号还大，
        # 说明最左边的页码号和第 1 页的页码号之间还有其它页码，因此需要显示省略号，通过 left_has_more 来指示。
        if left[0] > 2:
            left_has_more = True

        # 如果最左边的页码号比第 1 页的页码号大，说明当前页左边的连续页码号中不包含第一页的页码，
        # 所以需要显示第一页的页码号，通过 first 来指示
        if left[0] > 1:
            first = True
    else:
        # 用户请求的既不是最后一页，也不是第 1 页，则需要获取当前页左右两边的连续页码号，
        # 这里只获取了当前页码前后连续两个页码，你可以更改这个数字以获取更多页码。
        left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]
        right = page_range[page_number:page_number + list_num]

        # 是否需要显示最后一页和最后一页前的省略号
        if right[-1] < total_pages - 1:
            right_has_more = True
        if right[-1] < total_pages:
            last = True

        # 是否需要显示第 1 页和第 1 页后的省略号
        if left[0] > 2:
            left_has_more = True
        if left[0] > 1:
            first = True

    data = {
        'left': left,
        'right': right,
        'left_has_more': left_has_more,
        'right_has_more': right_has_more,
        'first': first,
        'last': last,
        'query_str': query_str,
        'page_obj': page,
    }

    return data


def get_zero_timestamp():
    """
    取当天0点的时间
    :return:
    """
    cur_timestamp = time.time()
    cur_time = time.localtime(cur_timestamp)
    zero_time_stamp = cur_timestamp - (
            cur_time.tm_sec + 60 * cur_time.tm_min + 3600 * cur_time.tm_hour)
    return zero_time_stamp


def get_days(days):
    """
    获取与当前日期相隔天数 可以为负
    :param days:
    :return:
    """
    now_date = datetime.datetime.fromtimestamp(get_zero_timestamp())
    return now_date + datetime.timedelta(days=days)


def multiple_replace(text, adict):
    """
    text = "Larry Wall is the creator of Perl"
       adict = {
          "Larry Wall" : "Guido van Rossum",
          "creator" : "Benevolent Dictator for Life",
          "Perl" : "Python",
       }
    :param text:
    :param adict:
    :return:
    """
    rx = re.compile('|'.join(map(re.escape, adict)))

    def one_xlat(match):
        return adict[match.group(0)]

    return rx.sub(one_xlat, text)


def combine_folder(*args):
    urls = list()
    for item in args:
        p_tag = str(item).replace('/', '')
        urls.append(p_tag)
    return '/'.join(urls) + '/'


def strip_tags(html, invalid_tags):
    """
    删除html代码中指定标签
    e.g: invalid_tags = ['b', 'i', 'u']
    :param html: 原html
    :param invalid_tags: 要删除的标签
    :return: 处理完成的html
    """
    soup = BeautifulSoup(html, 'lxml')

    for tag in soup.findAll(True):
        if tag.name in invalid_tags:
            s = tag.string if tag.string else ''
            tag.replaceWith(s)

    return soup


def push_baidu(url, title, site):
    baidu_api = 'http://data.zz.baidu.com/urls?site={site_url}&token={token}'
    baidu_site_api = baidu_api.format(site_url=site.domain,
                                      token=site.siteproperty.baidu_site_token)
    headers = {
        'Content-Type': 'text/plain'
    }
    ret = requests.post(baidu_site_api, headers=headers, data=url)
    baidu_data = ret.json()
    # 写放记录表
    push_log = BaiduPushLog()
    push_log.site = site
    push_log.title = title
    push_log.url = url
    try:
        if baidu_data['success'] > 0:
            push_log.status = True
        else:
            push_log.status = False
    except Exception as e:
        print('Something wrong with push to baidu: %s' % str(e))
        push_log.status = False
    push_log.save()
    return baidu_data


def get_ip(request):
    if 'HTTP_X_FORWARDED_FOR' in request.META:
        ip = request.META['HTTP_X_FORWARDED_FOR']
    else:
        ip = request.META['REMOTE_ADDR']
    return ip
