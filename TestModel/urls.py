from django.urls import path,re_path
from django.conf.urls import url

from TestModel import views # 从自己的 app 目录引入 views
urlpatterns = [
    url(r'^userAdd/', views.userAdd),
    path('userQuery/', views.userQuery),
    path('add_book/', views.add_book),
    path('add_books/', views.add_books),
    path('login/', views.user_login),
    path('LoginOut/', views.login_out),
    path('Orders/', views.orders),
    path('OrderAdd/', views.order_add),
    path('OrderEdit/', views.order_edit),
    # path('OrderDetail/<int:id>', views.order_detail),
    path('OrderDetail/', views.order_detail),
    path('OrderDel/', views.order_del),

]