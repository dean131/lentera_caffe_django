from django.urls import path, include

from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('items', views.ItemModelViewSet, basename='item')
router.register('orders', views.OrderModelViewSet, basename='order')
router.register('orderitems', views.OrderItemModelViewSet, basename='orderitem')

urlpatterns = [
    path('', include(router.urls)),

    path('saw/', views.SawView.as_view(), name='saw'),
    path('get-pertanyaan/', views.PertanyaanView.as_view(), name='get_pertanyaan'),
    # path('add-kriteria/', views.add_kriteria, name='add_kriteria'),
    # path('add-item/', views.add_item, name='add_item'),
]