# Generated by Django 4.2 on 2023-05-25 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='brand',
            name='allowCustomersToSelectPageSize',
        ),
        migrations.RemoveField(
            model_name='brand',
            name='displayOrder',
        ),
        migrations.RemoveField(
            model_name='brand',
            name='isPublished',
        ),
        migrations.RemoveField(
            model_name='brand',
            name='pageSize',
        ),
        migrations.RemoveField(
            model_name='brand',
            name='pageSizeOptions',
        ),
        migrations.RemoveField(
            model_name='category',
            name='allowCustomersToSelectPageSize',
        ),
        migrations.RemoveField(
            model_name='category',
            name='displayOrder',
        ),
        migrations.RemoveField(
            model_name='category',
            name='fullName',
        ),
        migrations.RemoveField(
            model_name='category',
            name='includeInTopMenu',
        ),
        migrations.RemoveField(
            model_name='category',
            name='isPublished',
        ),
        migrations.RemoveField(
            model_name='category',
            name='limitedToStores',
        ),
        migrations.RemoveField(
            model_name='category',
            name='pageSize',
        ),
        migrations.RemoveField(
            model_name='category',
            name='pageSizeOptions',
        ),
        migrations.RemoveField(
            model_name='category',
            name='showOnHomepage',
        ),
        migrations.RemoveField(
            model_name='category',
            name='subjectToAcl',
        ),
        migrations.AlterField(
            model_name='brand',
            name='titleEn',
            field=models.CharField(db_index=True, max_length=300, verbose_name='عنوان'),
        ),
        migrations.AlterField(
            model_name='category',
            name='titleEn',
            field=models.CharField(db_index=True, max_length=300, verbose_name='عنوان'),
        ),
        migrations.AlterField(
            model_name='product',
            name='nameEn',
            field=models.CharField(db_index=True, max_length=300, verbose_name='عنوان'),
        ),
    ]
