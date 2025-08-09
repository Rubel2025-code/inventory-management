from django.db import models
from django.contrib.auth.models import User
from inventory.models import Product

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Cart of {self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def subtotal(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.quantity} × {self.product.name}"

class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Rejected', 'Rejected'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE)
    transaction_number = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"
