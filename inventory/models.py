from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    stock = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    added_on = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="products/", blank=True, null=True)

    # ✅ New fields for supplier
    supplier_name = models.CharField(max_length=150, blank=True, null=True)
    supplier_contact = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.name
