from django.db import models
from django.contrib.auth.models import User
from inventory.models import Product

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def subtotal(self):
        return self.product.price * self.quantity

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction_number = models.CharField(max_length=100)
    items = models.ManyToManyField('orders.CartItem')
    created_at = models.DateTimeField(auto_now_add=True)

    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Rejected', 'Rejected'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    def ordered_items_list(self):
        """Return product names and quantities for display"""
        return [f"{item.product.name} ({item.quantity})" for item in self.items.all()]