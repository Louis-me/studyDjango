from .view import test_view, login_view, view_case, view_order, view_suite, timing_task_view, fuzz_view, \
    real_time_task_view, report_view, api_login_view, log_view


def user_login(request):
    return login_view.user_login(request)


def login_out(request):
    return login_view.login_out(request)


def orders(request):
    return view_order.orders(request)


def order_add(request):
    return view_order.order_add(request)


def order_edit(request):
    return view_order.order_edit(request)


def order_detail(request):
    return view_order.order_detail(request)


def order_del(request):
    return view_order.order_del(request)


def suites(request):
    return view_suite.suites(request)

def get_all_suite(request):
    return view_suite.get_all_suite(request)

def suite_add(request):
    return view_suite.suite_add(request)


def suite_edit(request):
    return view_suite.suite_edit(request)


def suite_del(request):
    return view_suite.suite_del(request)


def suite_detail(request):
    return view_suite.suite_detail(request)


def cases(request):
    return view_case.get_case_list(request)


def case_add(request):
    return view_case.case_add(request)


def case_del(request):
    return view_case.case_del(request)


def case_edit(request):
    return view_case.case_edit(request)


def case_detail(request):
    return view_case.case_detail(request)


def case_all(request):
    return view_case.case_all(request)


def suite_to_case_list(request):
    return view_case.suite_to_case_list(request)


def suite_set_case(request):
    return view_case.suite_set_case(request)


def get_shop_list(request):
    return test_view.get_shop_list(request)


def shop_detail(request, id):
    return test_view.shop_detail(request, id)


def shop_add(request):
    return test_view.shop_add(request)


# ----------------
def get_fuzz_list(request):
    """
    模糊用例规则
    """
    return fuzz_view.get_fuzz_list(request)


def fuzz_add(request):
    """
    新增模糊用例规则
    """
    return fuzz_view.fuzz_add(request)


def fuzz_detail(request):
    """
    模糊用例详情
    """
    return fuzz_view.fuzz_detail(request)


def fuzz_edit(request):
    """
    用例编辑
    """
    return fuzz_view.fuzz_edit(request)


def fuzz_del(request):
    """
    用例删除
    """
    return fuzz_view.fuzz_del(request)


def get_timing_task_list(request):
    """
    获取定时任务列表
    """
    return timing_task_view.get_timing_task_list(request)


def new_timing_task(request):
    """
    新建定时任务
    """
    return timing_task_view.new_timing_task(request)


def timing_task_del(request):
    """
    删除定时任务
    """
    return timing_task_view.timing_task_del(request)


def get_real_time_task_list(request):
    """
    实时任务列表
    """
    return real_time_task_view.get_real_time_task_list(request)


def new_real_time_task(request):
    """
    新建实时任务
    """
    return real_time_task_view.new_real_time_task(request)


def real_time_task_detail(request):
    """
    实时任务详情
    id为task得id
    """
    return real_time_task_view.real_time_task_detail(request)


def real_time_task_del(request):
    """
    删除实时任务
    """
    return real_time_task_view.real_time_task_del(request)

def get_login_api(request):
    """
    获取存在的登录信息
    """
    return api_login_view.get_login_api(request)

def login_test(request):
    """
    测试接口模拟登录，进行测试查看登录参数是否正常
    """
    return api_login_view.login_test(request)

def login_save(request):
    """
    测试接口模拟登录保存数据
    """
    return api_login_view.login_save(request)

def api_test(request):
    """
    测试接口,需要提前登录
    """
    return api_login_view.api_test(request)

def reports_module_case(request):
    """
    测试报告-图形展示-模块用例数量
    """
    return report_view.reports_module_case(request)


def reports_top_10_slow(request):
    """
    响应时间最慢的top10
    """
    return report_view.reports_top_10_slow(request)


def reports_top_slow_export(request):
    """
   导出top10最慢的接口信息
   """
    return report_view.reports_top_slow_export(request)


def report_task(request):
    """
    测试报告-图形展示-每个任务中的成功和失败用例
    """
    return report_view.report_task(request)


def reports_list(request):
    """
        测试报告-所有的测试报告列表
        """
    return report_view.reports_list(request)


def report_export(request, id):
    """
    导出测试报告为excel
    id 为report的id
    """
    return report_view.report_export(request, id)


def reports_detail(request):
    """
    测试报告详情
    id为report的id
    """
    return report_view.reports_detail(request)


def report_detail_del(request):
    """
    删除测试报告
    """
    return report_view.report_detail_del(request)


def logs(request):
    return log_view.logs(request)


def log_content(request):
    return log_view.log_content(request)
