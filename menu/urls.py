from django.urls import path
from . import views

app_name = 'menu'

urlpatterns = [
    path('', views.menu_list, name='menu_list'),
    path('item/<int:pk>/', views.food_detail, name='food_detail'),
]
