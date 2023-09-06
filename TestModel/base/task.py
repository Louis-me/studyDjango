# -*- coding: utf-8 -*-
import ast
import json
import time
from datetime import datetime

import requests
from django.http import JsonResponse

from ..base.fuzz_param import BaseFuzzParams
from ..models import Case, Suite, Report, ApiLogin
from ..base.element import Element


class ApiTask(object):
    @staticmethod
    def get_case_total_time(start_time, end_time):
        """
        得到用例的总耗时，统计格式为：hh-mm-ss
        :param start_time:  datetime.now().strftime("%H-%M-%S")
        :param end_time:
        :return:
        """
        formats = "%H-%M-%S"
        total_time = datetime.strptime(end_time, formats) - datetime.strptime(start_time, formats)
        return str(total_time)

    @staticmethod
    def get_case_total_time_ms(start_time, end_time):
        """
        得到每个用例耗时，统计单位为毫秒
        :param start_time:  datetime.datetime.now()
        :param end_time:
        :return:
        """
        total_time = (end_time - start_time).seconds * 1000 + (end_time - start_time).microseconds / 1000
        return str(total_time) + "ms"

    @classmethod
    def exec_case_background(cls, case_entry, _report, is_fuzz, lg_session):
        """
        :param case_entry 套件下关联的用例的实例类
        :param _report 新建测试总报告的实体类
        :param is_fuzz 是否开启fuzz
        :param lg_session 接口登录后的session
        后台执行任务,记录用例详情
        """

        protocol = case_entry.protocol
        name = case_entry.name
        method = case_entry.method
        params = case_entry.params
        hope = case_entry.hope
        hopes = hope.split("|")
        url = case_entry.url
        sum_pass = 0
        sum_fail = 0
        # print(protocol + "://" + url)
        # print(params)
        if params:
            params1 = ast.literal_eval(params)
        else:
            params1 = {}
        # 如果有参数和is_fuzz为真,就进行模糊测试
        if params1 and is_fuzz:
            f_code = 1
            for j in BaseFuzzParams().param_fi(params1):
                hope1 = ""
                hopes2 = ""
                name1 = "[模糊测试_%s]_%s" % (j["info"], name)
                # 为1表示所有参数为真,取正向场景的检查点,因为默认第一条数据就是正向场景
                if f_code == 1:
                    hope1 = hope
                    hopes2 = hopes
                    name1 = name
                f_code = 2
                s_time = datetime.now().strftime("%H-%M-%S")
                resp = cls().request_(method, protocol, url, j, lg_session)
                e_time = datetime.now().strftime("%H-%M-%S")
                sum_time = ApiTask.get_case_total_time(s_time, e_time)
                app = {"resp": resp, "sum_time": sum_time, "hopes": hopes2, "url": url, "protocol": protocol,
                       "params": j, "_report": _report, "name": name1,"method": method, "hope": hope1}
                result = cls.sum_report_item(app)

                # 同级用例结果
                if result == 1:
                    sum_pass += 1
                else:
                    sum_fail += 1
        else:
            s_time = datetime.now().strftime("%H-%M-%S")
            # 进行正常测试
            resp = cls().request_(method, protocol, url, params1,lg_session)
            e_time = datetime.now().strftime("%H-%M-%S")
            sum_time = ApiTask.get_case_total_time(s_time, e_time)

            app = {"resp": resp, "sum_time": sum_time, "hopes": hopes, "url": url, "protocol": protocol,
                   "params": params1, "_report": _report, "name": name,
                   "method": method, "hope": hope}

            result = cls().sum_report_item(app)

            # 所有用例的结果统计
            if result == 1:
                # sum_pass = 1
                sum_pass += 1
            else:
                sum_fail += 1

        return {"sum_pass": sum_pass, "sum_fail": sum_fail}

    @classmethod
    def request_(cls,method, protocol, url, params1, lg_session):
        """
        method: 请求方法
        protocol: 请求协议
        url
        params1: 入参
        lg_session： 登录后的session
        """

        headers = {'Content-Type': "application/json", "Authorization": "shikun"}
        resp = {"status_code": -1, "text": ""}
        # 后续要关闭
        time.sleep(2)
        try:
            if method == "post":
                res = lg_session.post(url=protocol + "://" + url, json=params1, headers=headers)
            elif method == "get":
                res = lg_session.get(url=protocol + "://" + url, params=params1, headers=headers)
            else:
                print("只支持get,post")
                res = {}
            resp["status_code"] = res.status_code
            resp["text"] = res.text
            return resp
        except Exception as e:
            resp["text"] = '{"error":"%s"}' %(str(e))
            return resp

    @classmethod
    def sum_report_item(cls, kwargs):
        """
        每个用例的执行情况写入测试报告详情页
        """
        resp1 = kwargs.get("resp")  # 请求后返回的数据
        hopes = kwargs.get("hopes")  # 已经切割好的期望结果[]
        # 把hopes转为dict
        hopes1 = {}
        if hopes and hopes[0] != "":
            for i in hopes:
                j = i.split(":")
                hopes1[j[0]] = j[1]

        hope = kwargs.get("hope")  # 期望结果
        url = kwargs.get("url")
        protocol = kwargs.get("protocol")  # 协议
        params = kwargs.get("params")  # 入参
        method = kwargs.get("method")  # 请求方法
        _report = kwargs.get("_report")  # 新建用例总报告后的实体类
        name = kwargs.get("name")  # 用例名字
        sum_time = kwargs.get("sum_time")
        # 用例检查结果
        is_check = Element.CASE_CHECK_SUCCESS

        if resp1["status_code"] == 200:
            # separators 表示去掉字典转换为字符中的空格
            # resp = json.dumps(json.loads(res.text), separators=(',', ':'))
            resp_ex = json.loads(resp1["text"])  # 实际结果
            # is_check = 1  # 0表示期望值不存在，没有进行检查;1成功;-1失败
            if len(hopes1) and len(hope):
                # is_check = -1
                is_check = Element.CASE_CHECK_FAIL
                # 循环检查期望值是否在实际值中能找到
                for j in hopes1:
                    int_hope = -1
                    str_hope = hopes1[j]
                    try:
                        int_hope = int(hopes1[j])
                    except Exception as e:
                        pass
                    # 现在前端传来的数据都为字符串，先转换为int后进行测试，后续优化
                    if int_hope == resp_ex[j] or str_hope == resp_ex[j]:
                        # is_check = 1
                        is_check = Element.CASE_CHECK_SUCCESS
                        break
            else:
                # 如果没有期望值，一般都是模糊用例，直接判断返回的code为200就算通过
                # is_check = Element.CASE_CHECK_DEFAULT
                pass
        else:
            # 响应结果若不为200,表示用例执行失败
            is_check = Element.CASE_CHECK_FAIL
        # 新建测试报告详情，写测试接口的值
        _report.reportitem_set.create(name=name, url=url, protocol=protocol, method=method,
                                      params=str(params)
                                      , hope=hope, sum_time=sum_time, fact=resp1,
                                      result=is_check)
        return is_check

    @classmethod
    def background_task(cls, suite_id, task, lg_session):
        """
        后台执行的任务：获取套件-获取套件下的用例
        suite_id: 套件id
        task: 任务实体类
        lg_session: 接口登录成功后的session
        """
        task_id = task.id
        # 如果为定时任务,那么执行的开始时间重新获取并保存
        if task.task_type == Element.TASK_TYPE_TIME:
            task.start_time = datetime.now().strftime("%H-%M-%S")
        # 更新任务为测试中
        task.task_state = Element.TASK_STATE_PROGRESS
        task.save()
        # 得到套件
        su = Suite.objects.get(id=suite_id)
        # 是否开启fuzz测试
        is_fuzz = su.is_fuzz
        # 得到套件下关联的用例
        ss = su.suitesetcase_set.all()
        # 获取用例执行的开始时间
        start_time = task.start_time
        # 新建一个测试报告
        _report = Report(name=task.name, start_time=start_time, task_id=task_id)
        _report.save()
        # 成功,失败例总数
        sum_pass = 0
        sum_fail = 0
        if not ss:
            print("==没有可用用例==")
        for i in ss:
            # time.sleep(2)
            case_id = i.case_id
            case_entry = Case.objects.get(pk=case_id)
            bac = cls().exec_case_background(case_entry, _report, is_fuzz, lg_session)
            sum_pass = sum_pass + bac["sum_pass"]
            sum_fail = sum_fail + bac["sum_fail"]

        end_time = datetime.now().strftime("%H-%M-%S")

        # 以小时，分钟，秒钟的方式记录所有用例耗时时间
        total_time = cls().get_case_total_time(start_time, end_time)
        # 再次编辑测试报告
        _report.sum_time = total_time
        _report.sum_pass = sum_pass
        _report.sum_fail = sum_fail
        _report.save()

        task_sum_time = ApiTask.get_case_total_time(task.start_time, end_time)
        # 回写任务已经完成
        task.task_state = Element.TASK_STATE_FINISH
        task.sum_time = task_sum_time
        task.save()

    @classmethod
    def check_api_login(cls):
        """
        对接口进行测试前需要检查登录接口是否正常
        """
        result = {"res": "", "is_success": False}
        headers = {'Content-Type': "application/json", "Authorization": "shikun"}
        try:
            # 对接口测试前,需要提前登录
            lg = ApiLogin.objects.get(pk=1)
            if not lg:
                return result
            param = json.loads(lg.params)
            req_s = requests.session()
            resp_l = req_s.post(lg.url, json=param, headers=headers)
            resp_l_json = json.loads(resp_l.text)
            if resp_l.status_code != 200 or resp_l_json.get("code") != 1:
                return result
        except Exception as e:
            return False
        result["res"] = req_s
        result["is_success"] = True
        return result
