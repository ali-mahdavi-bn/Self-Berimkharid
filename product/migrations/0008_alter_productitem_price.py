# Generated by Django 4.2 on 2023-06-04 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0007_alter_productitem_price_alter_productitem_recordedat'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productitem',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True),
        ),
    ]
