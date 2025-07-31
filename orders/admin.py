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
    list_display = ('user', 'transaction_number', 'status', 'created_at', 'ordered_items')
    list_editable = ('status',)  # ✅ Make status editable in list view
    list_filter = ('status', 'created_at')
    search_fields = ('transaction_number', 'user__username')

    def ordered_items(self, obj):
        """Show ordered products and quantities in admin list"""
        return ", ".join([f"{item.product.name} ({item.quantity})" for item in obj.items.all()])
    ordered_items.short_description = "Ordered Items"
