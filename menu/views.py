from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import FoodItem, Category


def home(request):
    featured_items = FoodItem.objects.filter(is_available=True)[:6]
    categories = Category.objects.filter(is_active=True)
    return render(request, 'home.html', {
        'featured_items': featured_items,
        'categories': categories,
    })


def menu_list(request):
    items = FoodItem.objects.filter(is_available=True).select_related('category')
    categories = Category.objects.filter(is_active=True)

    query = request.GET.get('q', '').strip()
    category_id = request.GET.get('category', '')

    if query:
        items = items.filter(Q(name__icontains=query) | Q(description__icontains=query))

    if category_id:
        items = items.filter(category_id=category_id)

    return render(request, 'menu/menu_list.html', {
        'items': items,
        'categories': categories,
        'query': query,
        'selected_category': category_id,
    })


def food_detail(request, pk):
    item = get_object_or_404(FoodItem, pk=pk)
    related_items = FoodItem.objects.filter(category=item.category, is_available=True).exclude(pk=pk)[:4]
    return render(request, 'menu/food_detail.html', {'item': item, 'related_items': related_items})
