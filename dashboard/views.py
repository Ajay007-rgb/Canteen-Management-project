from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Sum, Count, Q
from django.utils import timezone
from django.views.decorators.http import require_POST
import json

from .decorators import admin_required
from menu.models import FoodItem, Category
from menu.forms import FoodItemForm, CategoryForm
from orders.models import Order, OrderItem


@admin_required
def dashboard_home(request):
    today = timezone.now().date()

    total_users = User.objects.filter(is_staff=False).count()
    total_food_items = FoodItem.objects.count()
    total_orders = Order.objects.count()
    pending_orders = Order.objects.filter(status='pending').count()
    completed_orders = Order.objects.filter(status='completed').count()
    todays_orders = Order.objects.filter(created_at__date=today)
    todays_orders_count = todays_orders.count()
    todays_revenue = todays_orders.aggregate(total=Sum('total_amount'))['total'] or 0

    # Last 7 days orders + revenue for the chart
    last_7_days = []
    for i in range(6, -1, -1):
        day = today - timezone.timedelta(days=i)
        day_orders = Order.objects.filter(created_at__date=day)
        last_7_days.append({
            'label': day.strftime('%d %b'),
            'orders': day_orders.count(),
            'revenue': float(day_orders.aggregate(total=Sum('total_amount'))['total'] or 0),
        })

    # Popular food items by quantity sold
    popular_items = (
        OrderItem.objects.values('food_name')
        .annotate(total_qty=Sum('quantity'))
        .order_by('-total_qty')[:5]
    )

    context = {
        'total_users': total_users,
        'total_food_items': total_food_items,
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'completed_orders': completed_orders,
        'todays_orders_count': todays_orders_count,
        'todays_revenue': todays_revenue,
        'chart_labels': json.dumps([d['label'] for d in last_7_days]),
        'chart_orders': json.dumps([d['orders'] for d in last_7_days]),
        'chart_revenue': json.dumps([d['revenue'] for d in last_7_days]),
        'popular_labels': json.dumps([p['food_name'] for p in popular_items]),
        'popular_data': json.dumps([p['total_qty'] for p in popular_items]),
    }
    return render(request, 'dashboard/dashboard.html', context)


# ---------------------------------------------------------------------------
# Food management
# ---------------------------------------------------------------------------
@admin_required
def food_management(request):
    items = FoodItem.objects.select_related('category').all()
    query = request.GET.get('q', '').strip()
    if query:
        items = items.filter(Q(name__icontains=query))
    return render(request, 'dashboard/food_management.html', {'items': items, 'query': query})


@admin_required
def food_create(request):
    if request.method == 'POST':
        form = FoodItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Food item added successfully.')
            return redirect('dashboard:food_management')
    else:
        form = FoodItemForm()
    return render(request, 'dashboard/food_form.html', {'form': form, 'title': 'Add Food Item'})


@admin_required
def food_edit(request, pk):
    item = get_object_or_404(FoodItem, pk=pk)
    if request.method == 'POST':
        form = FoodItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Food item updated successfully.')
            return redirect('dashboard:food_management')
    else:
        form = FoodItemForm(instance=item)
    return render(request, 'dashboard/food_form.html', {'form': form, 'title': f'Edit {item.name}'})


@admin_required
@require_POST
def food_delete(request, pk):
    item = get_object_or_404(FoodItem, pk=pk)
    item.delete()
    messages.info(request, 'Food item deleted.')
    return redirect('dashboard:food_management')


# ---------------------------------------------------------------------------
# Category management
# ---------------------------------------------------------------------------
@admin_required
def category_management(request):
    categories = Category.objects.annotate(item_count=Count('food_items'))
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category added successfully.')
            return redirect('dashboard:category_management')
    else:
        form = CategoryForm()
    return render(request, 'dashboard/category_management.html', {'categories': categories, 'form': form})


@admin_required
@require_POST
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    messages.info(request, 'Category deleted.')
    return redirect('dashboard:category_management')


# ---------------------------------------------------------------------------
# Order management
# ---------------------------------------------------------------------------
@admin_required
def order_management(request):
    orders = Order.objects.select_related('user').prefetch_related('items').all()
    status_filter = request.GET.get('status', '')
    if status_filter:
        orders = orders.filter(status=status_filter)
    return render(request, 'dashboard/order_management.html', {
        'orders': orders,
        'status_choices': Order.STATUS_CHOICES,
        'status_filter': status_filter,
    })


@admin_required
@require_POST
def order_update_status(request, pk):
    order = get_object_or_404(Order, pk=pk)
    new_status = request.POST.get('status')
    if new_status in dict(Order.STATUS_CHOICES):
        order.status = new_status
        order.save()
        messages.success(request, f'Order {order.order_number} marked as {order.get_status_display()}.')
    return redirect('dashboard:order_management')


# ---------------------------------------------------------------------------
# User management
# ---------------------------------------------------------------------------
@admin_required
def user_management(request):
    users = User.objects.filter(is_staff=False).select_related('profile').order_by('-date_joined')
    return render(request, 'dashboard/user_management.html', {'users': users})
