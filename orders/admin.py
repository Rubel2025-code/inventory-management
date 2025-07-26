from django.contrib import admin
from .models import Cart, CartItem, Order

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user']

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart', 'product', 'quantity']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'transaction_number', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['transaction_number', 'user__username']
    filter_horizontal = ['items']
