import json

import django
from django.core.exceptions import ObjectDoesNotExist
from django.forms import model_to_dict
from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from django.shortcuts import render

# Create your views here.
from TestModel import models
from TestModel.models import Test, Users


def userAdd(request):
    test1 = Test(name='runoob')
    test1.save()
    return HttpResponse("<p>数据添加成功！</p>")


def userQuery(request):
    # 初始化
    response = ""
    response1 = ""

    # 通过objects这个模型管理器的all()获得所有数据行，相当于SQL中的SELECT * FROM
    list = Test.objects.all()

    # filter相当于SQL中的WHERE，可设置条件过滤结果
    response2 = Test.objects.filter(id=1)

    # 获取单个对象
    response3 = Test.objects.get(id=1)

    # 限制返回的数据 相当于 SQL 中的 OFFSET 0 LIMIT 2;
    Test.objects.order_by('name')[0:2]

    # 数据排序
    Test.objects.order_by("id")

    # 上面的方法可以连锁使用
    Test.objects.filter(name="runoob").order_by("id")

    # 输出所有数据
    for var in list:
        response1 += var.name + " "
    response = response1
    return HttpResponse("<p>" + response + "</p>")


def add_book(request):
    #  获取出版社对象
    pub_obj = models.Publish.objects.filter(pk=1).first()
    #  给书籍的出版社属性publish传出版社对象
    book = models.Book.objects.create(title="菜鸟教程", price=200, pub_date="2010-10-10", publish=pub_obj)
    print(book, type(book))
    return HttpResponse(book)


def add_books(request):
    #  获取作者对象
    chong = models.Author.objects.filter(name="令狐冲").first()
    ying = models.Author.objects.filter(name="任盈盈").first()
    #  获取书籍对象
    book = models.Book.objects.filter(title="菜鸟教程").first()
    #  给书籍对象的 authors 属性用 add 方法传作者对象
    # 菜鸟教程这本书有两个作者
    book.authors.add(chong, ying)
    return HttpResponse(book)


def add_books_1(request):
    #  获取作者对象
    chong = models.Author.objects.filter(name="令狐冲").first()
    #  获取作者对象的id
    pk = chong.pk
    #  获取书籍对象
    book = models.Book.objects.filter(title="冲灵剑法").first()
    #  给书籍对象的 authors 属性用 add 方法传作者对象的id
    book.authors.add(pk)


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
            print(request.session["username"])
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