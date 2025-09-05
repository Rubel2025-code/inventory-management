from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0002_product_stock'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='supplier_name',
            field=models.CharField(max_length=100, blank=True, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='supplier_contact',
            field=models.CharField(max_length=50, blank=True, null=True),
        ),
    ]
