import json

from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.forms import model_to_dict
from django.http import JsonResponse
from ..base.element import Element
from ..models import Fuzz


def get_fuzz_list(request):
    """
    模糊用例规则
    """
    data = request.GET
    query = data.get("query")  # 查询条件
    page_num = data.get("pagenum")  # 当前页码
    page_size = data.get("pagesize")  # 每页显示多少条
    if query:
        fuzzs = Fuzz.objects.filter(name__contains=query)

    else:
        fuzzs = Fuzz.objects.all().order_by("-id")
    response = {}
    # 生成分页实例
    paginator = Paginator(fuzzs, page_size)
    # 获取数据总条数
    response['total_count'] = paginator.count
    # 每页显示条数
    response['page_size'] = page_size
    # 总共页数
    response['total_page'] = paginator.num_pages
    response["list"] = []
    try:
        users = paginator.page(page_num)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    # 当前多少页
    response['pageNum'] = users.number
    # 获取数据
    for i in users.object_list:
        # response["list"].append(
        #     {"name": i.name, "fuzz_type": i.fuzz_type, "id": i.id, "content": i.fuzz_content}
        # )
        response["list"].append(model_to_dict(i))
    res = {'code': 1, 'msg': '获取成功', 'data': response}
    # 将数据返回到页面
    return JsonResponse(res)


def fuzz_add(request):
    """
    新增模糊用例规则
    """
    data = json.loads(request.body)
    name = data.get("name")
    fuzz_type = data.get("fuzz_type")
    fuzz_content = data.get("fuzz_content", "-1")
    # 新增的数据 fuzz_type必须为0，内置的规则不为0，不能删除和修改
    if fuzz_type != Element.FUZZ_ADD_TYPE:
        res = {'code': -1, 'msg': 'fuzz_type传参错误'}
        return JsonResponse(res)
    if not name and fuzz_type == "-1":
        res = {'code': -1, 'msg': 'name,fuzz_type must be fill'}
        return JsonResponse(res)
    Fuzz(name=name, fuzz_type=fuzz_type, fuzz_content=fuzz_content).save()
    res = {'code': 1, 'msg': 'success'}
    return JsonResponse(res)


def fuzz_detail(request):
    """
    模糊用例详情
    """
    data = request.GET
    id = data.get("id")  # suite_id 套件id
    if not id:
        result = {'code': -1, 'msg': 'id must be fill'}
        return JsonResponse(result)
    try:
        fuzz_entry = Fuzz.objects.get(id=id)
        resp = {"name": fuzz_entry.name, "fuzz_type": fuzz_entry.fuzz_type, "fuzz_content": fuzz_entry.fuzz_content}
        res = {'code': 1, 'msg': 'success', "data": resp}
        return JsonResponse(res)
    except ObjectDoesNotExist:
        res = {'code': - 1, 'msg': 'id is no effect row'}
        return JsonResponse(res)


def fuzz_edit(request):
    """
    用例编辑
    """
    data = json.loads(request.body)
    id = data.get("id")
    name = data.get("name")
    fuzz_type = data.get("fuzz_type","-1")
    fuzz_content = data.get("fuzz_content")
    print(data)
    if fuzz_type != Element.FUZZ_ADD_TYPE:
        res = {'code': -1, 'msg': 'fuzz_type is error,must is 0'}
        return JsonResponse(res)

    if not name or not fuzz_content or fuzz_type == "-1":
        res = {'code': -1, 'msg': 'content,fuzz_type,name must be fill'}
        return JsonResponse(res)
    try:
        fuzz_entry = Fuzz.objects.get(id=id)
        fuzz_entry.name = name
        fuzz_entry.fuzz_type = fuzz_type
        fuzz_entry.fuzz_content = fuzz_content
        fuzz_entry.save()
        res = {'code': 1, 'msg': 'success'}
        return JsonResponse(res)

    except ObjectDoesNotExist:
        res = {'code': - 1, 'msg': 'id can not find a have effect data'}
        return JsonResponse(res)


def fuzz_del(request):
    """
    用例删除
    """
    data = json.loads(request.body)
    id = data.get("id")
    if not id:
        res = {'code': -1, 'msg': 'id must be fill'}
        return JsonResponse(res)
    try:
        case_entry = Fuzz.objects.get(id=id)
        if case_entry.fuzz_type != Element.FUZZ_ADD_TYPE:
            res = {'code': -1, 'msg': 'default fuzz rule cannot del'}
            return JsonResponse(res)
        case_entry.delete()
        res = {'code': 1, 'msg': 'success'}
        return JsonResponse(res)
    except ObjectDoesNotExist:
        res = {'code': - 1, 'msg': 'id can not find a have effect data'}
        return JsonResponse(res)
