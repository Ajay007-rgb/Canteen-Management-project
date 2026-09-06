from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.db import transaction
from cart.models import Cart
from .models import Order, OrderItem
import razorpay
from django.conf import settings


@login_required
def checkout(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    items = cart.items.select_related('food_item').all()

    if not items:
        messages.warning(request, 'Your cart is empty. Add some items before checking out.')
        return redirect('menu:menu_list')

    if request.method == 'POST':
        delivery_note = request.POST.get('delivery_note', '').strip()
        with transaction.atomic():
            order = Order.objects.create(
                user=request.user,
                total_amount=cart.subtotal,
                delivery_note=delivery_note,
                status='pending',
            )
            for ci in items:
                OrderItem.objects.create(
                    order=order,
                    food_item=ci.food_item,
                    food_name=ci.food_item.name,
                    price=ci.food_item.price,
                    quantity=ci.quantity,
                )
            items.delete()  # clear the cart now that the order exists in DB

        amount_in_paise = int(order.total_amount * 100)
        razorpay_order = razorpay_client.order.create({
            'amount': amount_in_paise,
            'currency': 'INR',
            'payment_capture': 1,
        })
        order.razorpay_order_id = razorpay_order['id']
        order.save()       


        return render(request, 'orders/payment.html', {
            'order': order,
            'razorpay_key_id': settings.RAZORPAY_KEY_ID,
            'amount_in_paise': amount_in_paise,
        })

    return render(request, 'orders/checkout.html', {'cart': cart, 'items': items})


@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).prefetch_related('items')
    return render(request, 'orders/my_orders.html', {'orders': orders})


@login_required
def order_tracking(request, order_id):
    order = get_object_or_404(Order, pk=order_id, user=request.user)
    steps = ['pending', 'preparing', 'ready', 'completed']
    current_index = steps.index(order.status) if order.status in steps else -1
    return render(request, 'orders/order_tracking.html', {
        'order': order,
        'steps': steps,
        'current_index': current_index,
    })

razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))