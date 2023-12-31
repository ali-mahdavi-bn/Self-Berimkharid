# Generated by Django 4.2 on 2023-05-19 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Upload',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=255)),
                ('bucketName', models.CharField(max_length=255)),
                ('path', models.CharField(max_length=255)),
                ('isActive', models.BooleanField(default=True, verbose_name='فعال / غیرفعال')),
                ('isDelete', models.BooleanField(default=False, verbose_name='حذف شده / نشده')),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
