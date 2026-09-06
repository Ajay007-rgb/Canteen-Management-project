from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('my-orders/', views.my_orders, name='my_orders'),
    path('track/<int:order_id>/', views.order_tracking, name='order_tracking'),
    path('verify-payment/', views.verify_payment, name='verify_payment'),
]
