from django.db import models
from django.utils.text import slugify

from accounts.models import User


class City(models.Model):
    title = models.CharField(max_length=100)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


# Create your models here.
class Vendor(models.Model):
    name = models.CharField(max_length=255)
    nameEn = models.CharField(max_length=255)
    metaName = models.CharField(max_length=255)
    metaKeywords = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    metaDescription = models.CharField(max_length=255)
    link = models.CharField(max_length=255)
    ownerId = models.ForeignKey(User, on_delete=models.CASCADE)
    cityId = models.ForeignKey(City, on_delete=models.CASCADE)
    iconId = models.ForeignKey('upload.Upload', on_delete=models.CASCADE, verbose_name="ایکون")
    pictureGallery = models.ManyToManyField('upload.Upload', related_name='vendor_pictureGallery',
                                            verbose_name='عکس ها')
    postingMethods = models.CharField(max_length=255)
    phoneNumber = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    latitude = models.CharField(max_length=255)
    longitude = models.CharField(max_length=255)
    zipCode = models.CharField(max_length=255)
    paymentMethods = models.CharField(max_length=255)
    orderTrackingMethods = models.CharField(max_length=255)
    eNamadIsValid = models.BooleanField(default=False, verbose_name='تایید شده  / تایید نشده')
    eNamadExpDateTime = models.DateTimeField(null=True)
    status = models.CharField(max_length=255)
    slug = models.SlugField(default="",
                            null=False,
                            db_index=True,
                            blank=True,
                            max_length=200, unique=True)
    isDelete = models.BooleanField(default=False, verbose_name='حذف شده / نشده')
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class ClickHistory(models.Model):
    productId = models.ForeignKey('product.Product', on_delete=models.CASCADE)
    vendorId = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    userAgent = models.CharField(max_length=100)
    ipv4 = models.CharField(max_length=100, null=True, blank=True)
    ipv6 = models.CharField(max_length=100, default=None, null=True, blank=True)
    browserName = models.CharField(max_length=100)
    deviceName = models.CharField(max_length=100, null=True, blank=True)
    deviceResolution = models.CharField(max_length=100, null=True, blank=True)
    sessionKey = models.CharField(max_length=100, null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
