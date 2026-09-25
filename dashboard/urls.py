from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_home, name='dashboard_home'),
    path('food/', views.food_management, name='food_management'),
    path('food/add/', views.food_create, name='food_create'),
    path('food/<int:pk>/edit/', views.food_edit, name='food_edit'),
    path('food/<int:pk>/delete/', views.food_delete, name='food_delete'),
    path('categories/', views.category_management, name='category_management'),
    path('categories/<int:pk>/delete/', views.category_delete, name='category_delete'),
    path('orders/', views.order_management, name='order_management'),
    path('orders/<int:pk>/status/', views.order_update_status, name='order_update_status'),
    path('users/', views.user_management, name='user_management'),
    path('food-requests/', views.food_request_management, name='food_request_management'),
    path('food-requests/<int:pk>/status/', views.food_request_update_status, name='food_request_update_status'),
]
