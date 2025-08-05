from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    stock = models.PositiveIntegerField(default=0)  # ✅ Only one field for available units
    price = models.DecimalField(max_digits=10, decimal_places=2)
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
