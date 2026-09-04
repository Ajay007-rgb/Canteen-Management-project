from django.db import models
from django.contrib.auth.models import User
from menu.models import FoodItem


class Cart(models.Model):
    """Every user has exactly one persistent cart stored in the database
    (NOT in localStorage/session), so it survives across devices/logins."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart({self.user.username})"

    @property
    def total_items(self):
        return sum(ci.quantity for ci in self.items.all())

    @property
    def subtotal(self):
        return sum(ci.line_total for ci in self.items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('cart', 'food_item')

    def __str__(self):
        return f"{self.quantity} x {self.food_item.name}"

    @property
    def line_total(self):
        return self.food_item.price * self.quantity
