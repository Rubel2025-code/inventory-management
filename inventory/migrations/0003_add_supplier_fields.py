from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("inventory", "0002_product_stock"),  # adjust if your last migration has a different name
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="supplier_name",
            field=models.CharField(max_length=150, blank=True, null=True),
        ),
        migrations.AddField(
            model_name="product",
            name="supplier_contact",
            field=models.CharField(max_length=20, blank=True, null=True),
        ),
    ]
