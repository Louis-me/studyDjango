import json

import requests
from django.core.exceptions import ObjectDoesNotExist
from django.forms import model_to_dict
from django.http import JsonResponse

from ..models import ApiLogin


def get_login_api(request):
    """
    获取登录
    """
    lg = ApiLogin.objects.get(pk=1)
    if not lg:
        result = {'code': -1, 'msg': 'please check login param is success?'}
        return JsonResponse(result)

    return JsonResponse({'code': 1, 'msg': 'success', "data": model_to_dict(lg)})


def login_save(request):
    """
    测试api接口需要提前登陆的准备数据，默认在数据库新建一条数据
    """
    data = json.loads(request.body)
    url = data.get("url")
    params = data.get("params")
    method = "post"
    try:

        if not url or not params:
            return JsonResponse({'code': -1, 'msg': 'url,param,method must be fill'})
        l = ApiLogin.objects.get(pk=1)

        # 前端传过来的json若为单引号，替换为双引号
        if params:
            par = json.dumps(params)
            params = par.replace("'", "\"")
        l.url = url
        l.params = params
        l.save()

        result = {'code': 1, 'msg': '保存成功'}
        return JsonResponse(result)
    except ObjectDoesNotExist:

        result = {'code': -1, 'msg': '对象不存在'}
        return JsonResponse(result)


def login_test(request):
    """
    对api登陆接口进行测试，实际上此接口不存在，登录接口是其他接口
    """
    # data = json.loads(request.body)
    # print(data)
    # url = data.get('url')
    # test_params = data.get("params")
    # if not test_params or not url:
    #     result = {'code': -1, 'msg': "url and params must be fill"}
    #     return JsonResponse(result)

    result = {'code': 1, 'msg': "success"}
    return JsonResponse(result)


def api_test(request):
    try:
        lg = ApiLogin.objects.get(pk=1)
        if not lg:
            result = {'code': -1, 'msg': 'please check login param is success?'}
            return JsonResponse(result)
        param = json.loads(lg.params)
        req = requests.session()
        resp = req.post(lg.url, json=param)
        if resp.status_code == 200:
            # 设置请求头，防止白名单被拦截
            headers = {
                "Authorization": "shikun"
            }
            data = json.loads(request.body)
            url = data.get('url')
            method = data.get("method", "")
            test_params = data.get("params")
            if method.upper() == "POST":
                test_resp = req.post(url, json=test_params, headers=headers)
            else:
                test_resp = req.get(url, headers=headers)
            return JsonResponse(json.loads(test_resp.text))
        else:
            result = {"code": -1, "msg": "登录接口失败", "status_code": resp.status_code, "data": {"url": lg.url, "params": lg.params}}
            return JsonResponse(result)

    except Exception as e:
        result = {'code': -1, 'msg': str(e)}
        return JsonResponse(result)
