import ast
import json
import threading
import time
from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse
from ..models import Task, Report, Suite
from ..base.task import ApiTask
from ..base.element import Element
from ..base.base_log import log


def get_real_time_task_list(request):
    """
    实时任务列表
    """
    log.info("发起了实时任务列表")
    data = request.GET
    query = data.get("query")  # 查询条件
    page_num = data.get("pagenum")  # 当前页码
    page_size = data.get("pagesize")  # 每页显示多少条
    task_type = Element.TASK_TYPE_REAL
    if query:
        cases = Task.objects.filter(name__contains=query, task_type=task_type)

    else:
        cases = Task.objects.filter(task_type=task_type).order_by("-id")
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
        if i.task_state == Element.TASK_STATE_PROGRESS:
            task_state_name = "测试中"
        elif i.task_state == Element.TASK_STATE_FINISH:
            task_state_name = "测试完成"
        else:
            task_state_name = "未开始"
        try:
            suite_name = Suite.objects.get(id=i.suite_id).name
        except:
            suite_name = "没有值"
        try:
            # 得到测试总报告,获取用例数量统计，如果出现异常，可能是报告这里被删除了
            report = Report.objects.get(task_id=i.id)
            sum_pass = report.sum_pass
            sum_fail = report.sum_fail
            log.error("获取用例数量统计，如果出现异常，可能是报告这里被删除")
        except:
            sum_pass = 0
            sum_fail = 0

        response["list"].append(
            {"name": i.name, "id": i.id, "task_state_name": task_state_name, "sum_time": i.sum_time,
             "task_state": i.task_state, "suite_name": suite_name, "sum_pass": sum_pass, "sum_fail": sum_fail}
        )
    res = {'code': 1, 'msg': '获取成功', 'data': response}
    # 将数据返回到页面
    return JsonResponse(res)


def new_real_time_task(request):
    """
    新建实时任务
    """
    ch_login = ApiTask.check_api_login()
    if not ch_login["is_success"]:
        return JsonResponse({"code": -1, "msg": "请检查登录是否成功"})
    res_session = ch_login["res"]

    data = json.loads(request.body)
    name = data.get("name")
    task_state = Element.TASK_STATE_DEFAULT  # 默认未开始
    task_type = Element.TASK_TYPE_REAL  # 实时任务
    suite_id = data.get("suite_id")
    start_time = datetime.now().strftime("%H-%M-%S")
    ta = Task(name=name + "实时任务" + start_time, task_type=task_type, task_state=task_state, suite_id=suite_id,
              start_time=start_time)
    ta.save()
    res = {'code': 1, 'msg': 'success'}
    threading.Thread(target=ApiTask.background_task, args=(),
                     kwargs={"suite_id": suite_id, "task": ta, "lg_session": res_session}).start()
    # background_task(suite_id, ta)
    log.info("这是实时任务日志")
    return JsonResponse(res)


def real_time_task_detail(request):
    """
    实时任务详情
    """
    data = request.GET
    id = data.get("id")  # 查询条件
    if not id:
        return JsonResponse({'code': -1, 'msg': '%s is not exists' % id})
    # 得到测试总报告
    report = Report.objects.get(task_id=id)
    # 得到测试总报告下的测试详情
    report_items = report.reportitem_set.all()
    resp = []
    for i in report_items:
        url = i.protocol + "//" + i.url
        # 1通过，-1失败，-2不检查
        if i.result == 1:
            result = "通过"
        elif i.result == -1:
            result = "失败"
        else:
            result = "无检查点"
        params = i.params
        if params:
            params1 = ast.literal_eval(params)
        else:
            params1 = {}
        fact = i.fact
        if fact:
            fact1 = ast.literal_eval(fact)
        else:
            fact1 = {}

        app = {"url": url, "name": i.name, "method": i.method, "hope": i.hope, "fact": fact1,
               "result": result, "params": params1, "sum_time": i.sum_time}
        resp.append(app)
    data = {'code': 1, 'msg': 'success', "data": resp}
    return JsonResponse(data)


def real_time_task_del(request):
    """
    删除实时任务
    """
    data = json.loads(request.body)
    id = data.get("id")
    if not id:
        res = {'code': -1, 'msg': 'id must be fill'}
        return JsonResponse(res)
    try:
        task_entry = Task.objects.get(id=id)
        if task_entry.task_state == 2:
            task_entry.delete()
            res = {'code': 1, 'msg': 'success'}
        else:
            res = {'code': - 1, 'msg': 'task not finish,can not del'}
        return JsonResponse(res)
    except ObjectDoesNotExist:
        res = {'code': - 1, 'msg': 'id can not find a have effect data'}
        return JsonResponse(res)
