from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'stock', 'price', 'added_on','supplier_name','supplier_contact')
    list_editable = ('stock', 'price')  # Allow editing stock & price directly
    search_fields = ('name', 'category','supplier_name')
    list_filter = ('category', 'added_on')
    ordering = ('-added_on',)
