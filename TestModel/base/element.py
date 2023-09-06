# -*- coding=utf-8 -*-

import os

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)


class Element(object):
    REPORT_FILE = PATH("../Report/")  # 测试报告excel文件导出
    HOST = "http://127.0.0.1:8100/"
    FUZZ_ADD_TYPE = 0  # 新增的模糊用例规则必须为0
    FUZZ_DEL_TYPE = 1  # 内置模糊用例规则，删除此参数
    FUZZ_LONG_STR_TYPE = 2  # 内置模糊用例规则,超长字符串
    FUZZ_NO_PARAMS_TYPE = 3  # 内置模糊用例规则,参数不传
    # task_state  0没有在测试，1测试中，2测试完成
    TASK_STATE_DEFAULT = 0
    TASK_STATE_PROGRESS = 1
    TASK_STATE_FINISH = 2
    # task_type 1为实时任务，2为定时任务
    TASK_TYPE_REAL = 1
    TASK_TYPE_TIME = 2
    # 用例测试结果 # 0表示期望值不存在，没有进行检查;1成功;-1失败
    CASE_CHECK_DEFAULT = 0
    CASE_CHECK_SUCCESS = 1
    CASE_CHECK_FAIL = -1


