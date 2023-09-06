import json

from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.forms import model_to_dict
from django.http import JsonResponse

from ..models import Case, Suite, SuiteSetCase


def case_all(request):
    """
    所有用例列表
    """
    cases = Case.objects.all().order_by("-id")
    resp = []
    for i in cases:
        resp.append(model_to_dict(i))
    return JsonResponse({"code": 1, "msg": "success", "data": resp})


def get_case_list(request):
    """
    带分页和搜索的用例列表
    """
    data = request.GET
    query = data.get("query")  # 查询条件
    page_num = data.get("pagenum")  # 当前页码
    page_size = data.get("pagesize")  # 每页显示多少条
    if query:
        cases = Case.objects.filter(name__contains=query)

    else:
        cases = Case.objects.all().order_by("-id")
    response = {}
    # 生成分页实例
    paginator = Paginator(cases, page_size)
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
        url = i.protocol + "://" + i.url
        params= i.params
        if not params:
            params = '{}'
        response["list"].append(
            {"name": i.name, "url": url, "id": i.id,
             "method": i.method, "params": params, "hope": i.hope}
        )
    res = {'code': 1, 'msg': '获取成功', 'data': response}
    # 将数据返回到页面
    return JsonResponse(res)


def case_add(request):
    """
    新增用例
    """
    data = json.loads(request.body)
    name = data.get("name")
    url = data.get("url")
    protocol = data.get("protocol","http")
    method = data.get("method")
    params = data.get("params")
    # 前端传过来的json若为单引号，替换为双引号
    if params:
        par = json.dumps(params)
        params = par.replace("'", "\"")
    hope = data.get("hope")
    if not name or not url or not protocol or not protocol or not method or not hope:
        res = {'code': -1, 'msg': 'name,url,hope,method,protocol must be fill'}
        return JsonResponse(res)
    Case(name=name, url=url, protocol=protocol, params=params, method=method, hope=hope).save()
    res = {'code': 1, 'msg': 'success'}
    return JsonResponse(res)


def case_detail(request):
    """
    用例详情
    """
    data = request.GET
    id = data.get("id")  # 查询条件
    if not id:
        return JsonResponse({'code': -1, 'msg': '%s is not exists' % id})
    try:
        case_entry = Case.objects.get(id=id)
        params = case_entry.params
        resp = {"name": case_entry.name, "url": case_entry.url, "protocol": case_entry.protocol,
                "method": case_entry.method, "params": params, "hope": case_entry.hope}
        res = {'code': 1, 'msg': 'success', "data": resp}
        return JsonResponse(res)
    except ObjectDoesNotExist:
        res = {'code': - 1, 'msg': 'id is no effect row'}
        return JsonResponse(res)


def case_edit(request):
    """
    用例编辑
    """
    data = json.loads(request.body)
    id = data.get("id")
    name = data.get("name")
    url = data.get("url")
    protocol = data.get("protocol", "http")
    method = data.get("method")
    hope = data.get("hope")
    params = data.get("params")
    if not id or not name or not url or not protocol or not protocol or not method or not hope:
        res = {'code': -1, 'msg': 'id,name,url,hope,method,protocol must be fill'}
        return JsonResponse(res)
    try:
        # 前端传过来的json若为单引号，替换为双引号
        if params:
            par = json.dumps(params)
            params = par.replace("'", "\"")

        case_entry = Case.objects.get(id=id)
        case_entry.name = name
        case_entry.url = url
        case_entry.params = params
        case_entry.hope = hope
        case_entry.protocol = protocol
        case_entry.method = method
        case_entry.save()
        res = {'code': 1, 'msg': 'success'}
        return JsonResponse(res)

    except ObjectDoesNotExist:
        res = {'code': - 1, 'msg': 'id can not find a have effect data'}
        return JsonResponse(res)


def case_del(request):
    """
    用例删除
    """
    data = json.loads(request.body)
    id = data.get("id")
    if not id:
        res = {'code': -1, 'msg': 'id must be fill'}
        return JsonResponse(res)
    try:
        case_entry = Case.objects.get(id=id)
        case_entry.delete()
        res = {'code': 1, 'msg': 'success'}
        return JsonResponse(res)
    except ObjectDoesNotExist:
        res = {'code': - 1, 'msg': 'id can not find a have effect data'}
        return JsonResponse(res)

def suite_to_case_list(request):
    """

    套件已经关联的用例列表
    """
    data = request.GET
    suite_id = data.get("id")  # suite_id 套件id
    try:
        suite_set_cases = SuiteSetCase.objects.filter(suite_id=suite_id)
        cases = Case.objects.all()
        if not cases:
            result = {'code': -1, 'msg': 'case data is null'}
            return JsonResponse(result)
        resp = []
        for i in suite_set_cases:
            for j in cases:
                # 对比关联的id数据,只有在用例库中存在才展示
                if j.id == i.case_id:
                    resp.append({"case_id": i.case_id})
        return JsonResponse({"code": 1, "msg": "success", "data": resp})

    except ObjectDoesNotExist:
        result = {'code': -1, 'msg': 'no effect row'}
        return JsonResponse(result)


def suite_set_case(request):
    """
    套件关联用例
    """
    data = json.loads(request.body)
    suite_id = data.get("suite_id")
    case_ids = data.get("case_ids")  # [1,2,3,4]
    print(data)
    if not suite_id or not case_ids:
        result = {'code': -1, 'msg': 'suite_id and case_ids must be fill'}
        return JsonResponse(result)
    # 先删除当前关联的用例逻辑
    suite_set_cases = SuiteSetCase.objects.all()
    # suite_set_cases = SuiteSetCase.filter(suite_id=suite_id)
    for i in suite_set_cases:
        if i.suite_id == suite_id:
            try:
                entrys = SuiteSetCase.objects.filter(suite_id=suite_id)
                for j in entrys:
                    j.delete()
            except ObjectDoesNotExist:
                pass
    # 然后重新设置关联逻辑
    for i in case_ids:
        SuiteSetCase(suite_id=suite_id, case_id=i).save()

    result = {'code': 1, 'msg': 'success'}
    return JsonResponse(result)