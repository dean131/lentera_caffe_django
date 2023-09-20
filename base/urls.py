from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('', views.dashboard, name='dashboard'),
    path('customers-page', views.customers_page, name='customers_page'),
    path('cashier-page', views.cashier_page, name='cashier_page'),
    path('admin-page', views.admin_page, name='admin_page'),
    path('menu-page', views.menu_page, name='menu_page'),
    path('order-page', views.order_page, name='order_page'),
    path('cart-page', views.cart_page, name='cart_page'),
    path('notification-page', views.notification_page, name='notification_page'),
    path('saw-page', views.saw_page, name='saw_page'),
    path('kriteria-page', views.kriteria_page, name='kriteria_page'),
    path('subkriteria-page', views.subkriteria_page, name='subkriteria_page'),
]