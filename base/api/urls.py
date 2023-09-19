from django.urls import path

from . import views

urlpatterns = [
    path('saw/', views.saw, name='saw'),
    path('add-kriteria/', views.add_kriteria, name='add_kriteria'),
    path('add-item/', views.add_item, name='add_item'),
    path('get-pertanyaan/', views.get_pertanyaan, name='get_pertanyaan'),
]