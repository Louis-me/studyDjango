import json

from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse

from TestModel.models import Users


def user_login(request):
    if request.method != "POST":
        return JsonResponse({'code': -1, 'msg': 'method must is POST'})

    data = json.loads(request.body)
    user_name = data.get('username')
    pwd = data.get("password")
    try:
        user_entry = Users.objects.get(name=user_name, pwd=pwd)
        if user_entry:
            # 设置登录的session
            request.session["username"] = user_name
            return JsonResponse({'code': 1, 'msg': 'login is success'})
        else:
            return JsonResponse({'code': -1, 'msg': 'login is fail221'})
    except ObjectDoesNotExist:
        return JsonResponse({'code': -1, 'msg': 'login is fail111'})


def login_out(request):
    if request.session["username"]:
        del request.session['username']
        return JsonResponse({'code': 1, 'msg': 'success'})
    return JsonResponse({'code': -1, 'msg': 'session is not exists'})