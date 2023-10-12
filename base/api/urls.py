from django.urls import path

from . import views

urlpatterns = [
    path('saw/', views.SawView.as_view(), name='saw'),
    path('get-pertanyaan/', views.PertanyaanView.as_view(), name='get_pertanyaan'),
    # path('add-kriteria/', views.add_kriteria, name='add_kriteria'),
    # path('add-item/', views.add_item, name='add_item'),
]