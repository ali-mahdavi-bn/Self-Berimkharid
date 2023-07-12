# Generated by Django 4.2 on 2023-06-06 19:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_user_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdetails',
            name='birth',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='userdetails',
            name='gender',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='userdetails',
            name='lastLogin',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='userdetails',
            name='nationalCode',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]