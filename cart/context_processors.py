def cart_summary(request):
    """Makes the cart item count available in every template (for the
    navbar cart badge) without every view having to pass it explicitly."""
    count = 0
    if request.user.is_authenticated:
        cart = getattr(request.user, 'cart', None)
        if cart:
            count = cart.total_items
    return {'cart_item_count': count}
