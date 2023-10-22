from django.urls import path

from . import views


urlpatterns = [
    path('', views.dashboard, name='dashboard'),

    path('login-user/', views.login_user, name='login_user'),
    path('register-user/', views.register_user, name='register_user'),
    path('edit-user/', views.edit_user, name='edit_user'),
    path('delete-user/', views.delete_user, name='delete_user'),
    path('logout/', views.logout_user, name='logout_user'),

    path('customers-page/', views.customers_page, name='customers_page'),
    path('cashier-page/', views.cashier_page, name='cashier_page'),
    path('admin-page/', views.admin_page, name='admin_page'),

    path('order-page/', views.order_page, name='order_page'),
    path('order-history-page/', views.order_history_page, name='order_history_page'),
    path('notification-page/', views.notification_page, name='notification_page'),

    path('item-page/', views.item_page, name='item_page'),
    path('add-item/', views.add_item, name='add_item'),
    path('edit-item/', views.edit_item, name='edit_item'),
    path('delete-item/', views.delete_item, name='delete_item'),

    path('kriteria-page/', views.kriteria_page, name='kriteria_page'),
    path('add-kriteria/', views.add_kriteria, name='add_kriteria'),
    path('edit-kriteria/', views.edit_kriteria, name='edit_kriteria'),
    path('delete-kriteria/', views.delete_kriteria, name='delete_kriteria'),

    path('saw-page/', views.saw_page, name='saw_page'),

    path('subkriteria-page/', views.subkriteria_page, name='subkriteria_page'),
    path('add_subkriteria/', views.add_subkriteria, name='add_subkriteria'),
    path('edit_subkriteria/', views.edit_subkriteria, name='edit_subkriteria'),
    path('delete_subkriteria/', views.delete_subkriteria, name='delete_subkriteria'),
]