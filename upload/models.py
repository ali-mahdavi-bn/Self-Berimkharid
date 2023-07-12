from django.db import models


# from vendor.models import Vendor


# Create your models here.
class Upload(models.Model):
    type = models.CharField(max_length=255)
    bucketName = models.CharField(max_length=255)
    path = models.CharField(max_length=255)
    isActive = models.BooleanField(default=True, verbose_name='فعال / غیرفعال')
    isDelete = models.BooleanField(default=False, verbose_name='حذف شده / نشده')
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.bucketName