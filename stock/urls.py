from django.urls import path
from . import views

app_name = 'stock'

urlpatterns = [
    path('', views.list_data, name="list_data"),
    path('load_data/', views.load_data, name="load_data"),
    path('delete_data/', views.delete_data, name="delete_data"),
]
