import json

from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse

from TestModel import models


def orders(request):
    if request.method != "GET":
        return JsonResponse({'code': -1, 'msg': 'method must is GET'})

    data = request.GET
    query = data.get("query")  # 查询条件
    page_num = data.get("pagenum", 1)  # 当前页码
    page_size = data.get("pagesize", 10)  # 每页显示多少条
    if query:
        order_list = models.Order.objects.filter(name__contains=query)
    else:
        order_list = models.Order.objects.all().order_by("-updated_at")
    response = {}
    # 生成分页实例
    paginator = Paginator(order_list, page_size)
    # 获取数据总条数
    response['total_count'] = paginator.count
    # 每页显示条数
    response['page_size'] = page_size
    # 总共页数
    response['total_page'] = paginator.num_pages
    response["list"] = []

    try:
        orders_page = paginator.page(page_num)
    except PageNotAnInteger:
        orders_page = paginator.page(1)
    except EmptyPage:
        orders_page = paginator.page(paginator.num_pages)
        # 当前多少页
    response['pageNum'] = orders_page.number
    # 获取数据
    # response["list"] = orders_page.object_list
    t_l = list(orders_page.object_list)
    dt = []
    for i in t_l:
        # dt.append(model_to_dict(i)) 直接这样转造成日期丢失
        create_time = i.created_at.strftime('%Y-%m-%d %H:%M:%S')
        update_time = i.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        dt.append({"id": i.id, "name": i.name, "price": i.price, "desc": i.desc, "created_at": create_time,
                   "updated_at": update_time})

    response["list"] = dt
    res = {'code': 1, 'msg': '获取成功', 'data': response}
    # 将数据返回到页面
    return JsonResponse(res)


def order_add(request):
    if request.method != "POST":
        return JsonResponse({'code': -1, 'msg': 'method must is POST'})

    data = json.loads(request.body)

    keys = ["name", "desc", "price"]
    for i in keys:
        if i not in data.keys():
            return JsonResponse({'code': -1, 'msg': '%s is not exists' % i})
    name = data.get('name')
    desc = data.get('desc')
    price = data.get('price')
    order = models.Order(name=name, price=price, desc=desc)
    order.save()
    return JsonResponse({'code': 1, 'msg': 'success'})


def order_edit(request):
    if request.method != "POST":
        return JsonResponse({'code': -1, 'msg': 'method must is POST'})

    data = json.loads(request.body)

    keys = ["name", "desc", "price", "id"]
    for i in keys:
        if i not in data.keys():
            return JsonResponse({'code': -1, 'msg': '%s is not exists' % i})

    id = data.get('id')
    name = data.get('name')
    desc = data.get('desc')
    price = data.get('price')
    try:
        order_entry = models.Order.objects.get(id=id)
        order_entry.name = name
        order_entry.desc = desc
        order_entry.price = price
        order_entry.save()
        return JsonResponse({'code': 1, 'msg': 'success'})

    except ObjectDoesNotExist:
        return JsonResponse({'code': -1, 'msg': '数据不存在'})


def order_detail(request):
    if request.method != "GET":
        return JsonResponse({'code': -1, 'msg': 'method must is Get'})

    data = request.GET
    id = data.get("id")  # 查询条件
    if not id:
        return JsonResponse({'code': -1, 'msg': '%s is not exists' % id})
    try:
        order_entry = models.Order.objects.get(id=id)
        data = {"name": order_entry.name, "desc": order_entry.desc, "price": order_entry.price}
        return JsonResponse({'code': 1, 'msg': 'success', "data": data})

    except ObjectDoesNotExist:
        return JsonResponse({'code': -1, 'msg': '数据不存在'})


def order_del(request):
    if request.method != "POST":
        return JsonResponse({'code': -1, 'msg': 'method must is POST'})

    data = json.loads(request.body)
    id = data.get('id')
    if not id:
        return JsonResponse({'code': -1, 'msg': 'id is not exists'})
    try:
        order_entry = models.Order.objects.get(id=id)
        order_entry.delete()
        return JsonResponse({'code': 1, 'msg': 'success'})

    except ObjectDoesNotExist:
        return JsonResponse({'code': -1, 'msg': '数据不存在'})
