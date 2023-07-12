# Generated by Django 4.2 on 2023-05-19 07:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('upload', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('userName', models.CharField(max_length=255, unique=True)),
                ('firstName', models.CharField(max_length=50)),
                ('lastName', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('phoneNumber', models.CharField(max_length=11, unique=True)),
                ('type', models.CharField(max_length=50)),
                ('status', models.CharField(max_length=50)),
                ('isAdmin', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='VerifyUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phoneNumber', models.CharField(max_length=255)),
                ('email', models.CharField(max_length=255)),
                ('code', models.CharField(max_length=255)),
                ('isUsed', models.BooleanField(default=False)),
                ('mode', models.CharField(max_length=255)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.CharField(max_length=100)),
                ('nationalCode', models.CharField(max_length=100)),
                ('birth', models.DateTimeField()),
                ('lastLogin', models.DateTimeField()),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
                ('pictureId', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Upload_UserDetails', to='upload.upload')),
                ('userId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='userId_UserDetails', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
