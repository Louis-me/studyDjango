from django.http import JsonResponse
from django.shortcuts import redirect,render
from django.utils.deprecation import MiddlewareMixin
import re


#白名单
#将登陆、登出、验证登陆请求设为白名单，不进行用户验证。
#这里设置了/static/静态文件，因为我这个项目静态文件没走nginx，如果静态文件通过nginx访问，可以不需要设置
exclued_path = ["/login/","/testModel/login/","/logout/","/testModel/LoginOut/","/static/"]


#用来验证用户是否有权限登陆的中间件
class AuthenticationMiddle(MiddlewareMixin):
    def process_request(self, request):
        url_path = request.path
        print(url_path)
        #如果不在请求在白名单里
        if url_path not in exclued_path:
            #如果未登陆，则调转到登陆页面，将请求的url作为next参数
            # if  not request.user.is_authenticated:
            if not request.session.get("username"):
                # return redirect("/login/?next={url_path}".format(url_path=url_path))
                return JsonResponse({'code': 400, 'msg': 'login is failed2222'})
        #如果已经登陆，则通过
        else:
            pass
