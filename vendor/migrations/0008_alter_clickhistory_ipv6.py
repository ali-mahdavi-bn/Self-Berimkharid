# Generated by Django 4.2 on 2023-06-06 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0007_alter_clickhistory_ipv6'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clickhistory',
            name='ipv6',
            field=models.CharField(blank=True, default=None, max_length=100, null=True),
        ),
    ]
