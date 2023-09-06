from django.urls import path,re_path
from django.conf.urls import url

from TestModel import views # 从自己的 app 目录引入 views
urlpatterns = [
    path('login/', views.user_login),
    path('LoginOut/', views.login_out),
    path('Orders/', views.orders),
    path('OrderAdd/', views.order_add),
    path('OrderEdit/', views.order_edit),
    # path('OrderDetail/<int:id>', views.order_detail),
    path('OrderDetail/', views.order_detail),
    path('OrderDel/', views.order_del),
    path('suites/', views.suites),
    path('get_all_suite/', views.get_all_suite),

    path('suite_add/', views.suite_add),
    path('suite_edit/', views.suite_edit),
    path('suite_del/', views.suite_del),
    path('suite_detail/', views.suite_detail),
    path('cases/', views.cases),
    path('case_add/', views.case_add),
    path('case_edit/', views.case_edit),
    path('case_del/', views.case_del),
    path('case_detail/', views.case_detail),
    path('case_all/', views.case_all),
    path('suite_to_case_list/', views.suite_to_case_list),
    path('suite_set_case/', views.suite_set_case),
    url(r'^get_shop_list', views.get_shop_list),
    url(r'^shop_detail/<int:id>', views.shop_detail),
    url(r'^shop_add', views.shop_add),
    path('new_real_time_task/', views.new_real_time_task),
    path('get_real_time_task_list/', views.get_real_time_task_list),
    # path('real_time_task_detail/<int:id>/', views.real_time_task_detail),
    path('real_time_task_detail/', views.real_time_task_detail),
    path('real_time_task_del/', views.real_time_task_del),
    path('get_timing_task_list/', views.get_timing_task_list),
    path('new_timing_task/', views.new_timing_task),
    path('timing_task_del/', views.timing_task_del),
    path('reports_module_case/', views.reports_module_case),
    path('report_task/', views.report_task),
    path('reports_top_10_slow/', views.reports_top_10_slow),
    path('reports_top_slow_export/', views.reports_top_slow_export),
    path('reports_list/', views.reports_list),
    path('reports_detail/', views.reports_detail),
    path('report_detail_del/', views.report_detail_del),
    path('report_export/<int:id>/', views.report_export),
    url(r'^logs', views.logs),
    url(r'^log_content', views.log_content),
    path('get_fuzz_list/', views.get_fuzz_list),  # 模糊用例规则列表
    path('fuzz_add/', views.fuzz_add),  # 模糊用例规则添加
    path('fuzz_edit/', views.fuzz_edit),  # 模糊用例规则编辑
    path('fuzz_detail/', views.fuzz_detail),  # 模糊用例规则详情
    path('fuzz_del/', views.fuzz_del),  # 删除模糊用例规则详情
    path('login_save/', views.login_save),  # 测试接口模拟登录保存数据
    path('login_test/', views.login_test),  # 测试接口模拟登录
    path('api_test/', views.api_test),
    path('get_login_api/', views.get_login_api),
]