from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'stock', 'price', 'added_on')
    list_editable = ('stock', 'price')  # Allow editing stock & price directly
    search_fields = ('name', 'category')
    list_filter = ('category', 'added_on')
    ordering = ('-added_on',)
