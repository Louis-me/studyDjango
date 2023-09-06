import json

from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.forms import model_to_dict
from django.http import JsonResponse

from .. import models
from .. import models


def get_all_suite(request):
    resp = []
    suite_list = models.Suite.objects.all()
    for i in suite_list:
        resp.append({"id": i.id, "name": i.name})
    return JsonResponse({"code": 1, "msg": "success", "data": resp})


def suites(request):
    if request.method != "GET":
        return JsonResponse({'code': -1, 'msg': 'method must is GET'})

    data = request.GET
    query = data.get("query")  # 查询条件
    page_num = data.get("pagenum", 1)  # 当前页码
    page_size = data.get("pagesize", 10)  # 每页显示多少条
    if query:
        _list = models.Suite.objects.filter(name__contains=query)
    else:
        _list = models.Suite.objects.all().order_by("-updated_at")
    response = {}
    # 生成分页实例
    paginator = Paginator(_list, page_size)
    # 获取数据总条数
    response['total_count'] = paginator.count
    # 每页显示条数
    response['page_size'] = page_size
    # 总共页数
    response['total_page'] = paginator.num_pages
    response["list"] = []

    try:
        _page = paginator.page(page_num)
    except PageNotAnInteger:
        _page = paginator.page(1)
    except EmptyPage:
        _page = paginator.page(paginator.num_pages)
        # 当前多少页
    response['pageNum'] = _page.number
    # 获取数据
    t_l = list(_page.object_list)
    dt = []
    for i in t_l:
        dt.append(model_to_dict(i))

    response["list"] = dt
    res = {'code': 1, 'msg': '获取成功', 'data': response}
    # 将数据返回到页面
    return JsonResponse(res)

def suite_add(request):
    data = json.loads(request.body)
    name = data.get("name")
    is_fuzz = data.get("is_fuzz", False)
    models.Suite(name=name, is_fuzz=is_fuzz).save()
    result = {'code': 1, 'msg': 'success'}
    return JsonResponse(result)


def suite_edit(request):
    """
    编辑套件
    """
    data = json.loads(request.body)
    id = data.get("id")
    name = data.get("name")
    is_fuzz = data.get("is_fuzz", None)
    if not id or not name or is_fuzz is None:
        result = {'code': -1, 'msg': 'id,name,is_fuzz must be fill'}
        return JsonResponse(result)
    try:
        id = data.get("id")
        suite_entry = models.Suite.objects.get(id=id)
        if not suite_entry:
            result = {'code': -1, 'msg': 'no effect row'}
            return JsonResponse(result)
        suite_entry.is_fuzz = is_fuzz
        suite_entry.name = name
        suite_entry.save()
        return JsonResponse({'code': 1, 'msg': 'success'})
    except ObjectDoesNotExist:
        result = {'code': -1, 'msg': 'no effect row'}
        return JsonResponse(result)


def suite_detail(request):
    """
    套件详情
    """
    data = request.GET
    id = data.get("id")  # 查询条件
    if not id:
        return JsonResponse({'code': -1, 'msg': '%s is not exists' % id})
    try:
        suite_entry = models.Suite.objects.get(id=id)
        if not suite_entry:
            result = {'code': -1, 'msg': 'no effect row'}
            return JsonResponse(result)
        result = {'code': 1, 'msg': 'success', "data": {"name": suite_entry.name, "is_fuzz": suite_entry.is_fuzz}}
        return JsonResponse(result)

    except ObjectDoesNotExist:
        result = {'code': -1, 'msg': 'no effect row'}
        return JsonResponse(result)


def suite_del(request):
    """
    删除套件
    """
    data = json.loads(request.body)
    id = data.get("id")
    if not id:
        result = {'code': -1, 'msg': 'id must be fill'}
        return JsonResponse(result)
    try:
        suite_entry = models.Suite.objects.get(id=id)
        if not suite_entry:
            result = {'code': -1, 'msg': 'id is no effect row'}
            return JsonResponse(result)
        else:
            suite_entry.delete()
            result = {'code': 1, 'msg': 'success'}
            return JsonResponse(result)
    except ObjectDoesNotExist:
        result = {'code': -1, 'msg': 'no effect row'}
        return JsonResponse(result)