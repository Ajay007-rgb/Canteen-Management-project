from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from menu.models import FoodItem
from .models import Cart, CartItem


@login_required
def cart_detail(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    items = cart.items.select_related('food_item').all()
    return render(request, 'cart/cart.html', {'cart': cart, 'items': items})


@login_required
@require_POST
def add_to_cart(request, food_id):
    food_item = get_object_or_404(FoodItem, pk=food_id, is_available=True)
    cart, _ = Cart.objects.get_or_create(user=request.user)
    item, created = CartItem.objects.get_or_create(cart=cart, food_item=food_item)
    if not created:
        item.quantity += 1
    item.save()
    messages.success(request, f'{food_item.name} added to cart.')
    return redirect(request.POST.get('next', 'menu:menu_list'))


@login_required
@require_POST
def update_quantity(request, item_id):
    item = get_object_or_404(CartItem, pk=item_id, cart__user=request.user)
    action = request.POST.get('action')
    if action == 'increase':
        item.quantity += 1
        item.save()
    elif action == 'decrease':
        item.quantity -= 1
        if item.quantity <= 0:
            item.delete()
        else:
            item.save()
    return redirect('cart:cart_detail')


@login_required
@require_POST
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, pk=item_id, cart__user=request.user)
    item.delete()
    messages.info(request, 'Item removed from cart.')
    return redirect('cart:cart_detail')
