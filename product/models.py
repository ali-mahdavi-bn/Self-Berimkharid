from django.db import models
from django.utils.text import slugify

from django.db.models import JSONField


# from django.db.models import Max

# from vendor.models import Vendor


# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=300, db_index=True, verbose_name='عنوان')
    titleEn = models.CharField(max_length=300, db_index=True, verbose_name='عنوان')
    metaTitle = models.CharField(max_length=120)
    parentId = models.ForeignKey('self', null=True, blank=True, related_name='category_parent',
                                 on_delete=models.CASCADE,
                                 verbose_name='دسته بندی والد')
    metaKeywords = models.CharField(max_length=120)
    description = models.CharField(max_length=120)
    metaDescription = models.CharField(max_length=120)
    pictureId = models.ForeignKey('upload.Upload', on_delete=models.CASCADE, null=True,
                                  related_name='category_picture',
                                  verbose_name="عکس")

    slug = models.SlugField(default="",
                            null=False,
                            db_index=True,
                            blank=True,
                            max_length=200, unique=True)
    isActive = models.BooleanField(default=True, verbose_name='فعال / غیرفعال')
    isDelete = models.BooleanField(default=False, verbose_name='حذف شده / نشده')
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Brand(models.Model):
    title = models.CharField(max_length=120)
    titleEn = models.CharField(max_length=300, db_index=True, verbose_name='عنوان')
    metaTitle = models.CharField(max_length=120)
    metaKeywords = models.CharField(max_length=120)
    description = models.CharField(max_length=120)
    metaDescription = models.CharField(max_length=120)
    pictureId = models.ForeignKey('upload.Upload', related_name='brand_picture', on_delete=models.CASCADE,
                                  verbose_name="عکس")
    iconId = models.ForeignKey('upload.Upload', related_name='brand_icon', on_delete=models.CASCADE,
                               verbose_name="ایکون")
    slug = models.SlugField(default="",
                            null=False,
                            db_index=True,
                            blank=True,
                            max_length=200, unique=True)
    internal = models.BooleanField(default=True, verbose_name='برند داخلی / برند خارجی', null=True, blank=True, )
    isActive = models.BooleanField(default=True, verbose_name='فعال / غیرفعال')
    isDelete = models.BooleanField(default=False, verbose_name='حذف شده / نشده')
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Product(models.Model):
    name = models.CharField(max_length=300, verbose_name='نام محصول')
    nameEn = models.CharField(max_length=300, db_index=True, verbose_name='عنوان')
    metaTitle = models.CharField(max_length=120)
    metaKeywords = models.CharField(max_length=120)
    shortDescription = models.CharField(max_length=360, db_index=True, null=True, verbose_name='توضیحات کوتاه')
    description = models.TextField(verbose_name='توضیحات اصلی', db_index=True)
    metaDescription = models.CharField(max_length=120)
    status = models.CharField(max_length=255, default='published')
    pictureGallery = models.ManyToManyField('upload.Upload', related_name='product_pictureGallery',
                                            verbose_name='عکس ها')
    details = JSONField(null=True, blank=True)
    categoryId = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name='کتگوری', null=True, blank=True)
    brandId = models.ForeignKey('Brand', on_delete=models.CASCADE, verbose_name='برند', null=True, blank=True)
    slug = models.SlugField(default="",
                            null=False,
                            db_index=True,
                            blank=True,
                            max_length=200, unique=True)

    isUsed = models.BooleanField(verbose_name='کارکرده', default=False)
    showOnHomepage = models.BooleanField(default=True, verbose_name='نمایش در صفحه اصلی / عدم نمایش در صفحه اصلی')
    isActive = models.BooleanField(default=True, verbose_name='فعال / غیرفعال')
    isDelete = models.BooleanField(default=False, verbose_name='حذف شده / نشده')
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'

    def __str__(self):
        return self.name


class LatestProductItemManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().annotate(latest_recorded=Max('recordedAt'))


class ProductItem(models.Model):
    productId = models.ForeignKey('Product', related_name='productItem_product', on_delete=models.CASCADE)
    vendorId = models.ForeignKey('vendor.Vendor', related_name='productItem_vendor', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    link = models.CharField(max_length=255)
    inStock = models.BooleanField(default=True)
    recordedAt = models.DateTimeField()
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    # objects = LatestProductItemManager()


class FavoriteProduct(models.Model):
    productId = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='favoriteProduct_product')
    userId = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    minPrice = models.DecimalField(max_digits=10, decimal_places=2)
    maxPrice = models.DecimalField(max_digits=10, decimal_places=2)
    sendAlarm = models.BooleanField(default=False)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)


class Like(models.Model):
    productId = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='like_product', )
    userId = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='like_user')
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)


class PriceHistory(models.Model):
    productId = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='priceHistory_product')
    price = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    type = models.CharField(max_length=255)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)


class Comment(models.Model):
    productId = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='comment_product')
    userId = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='comment_user')
    parentId = models.ForeignKey('self', null=True, blank=True,
                                 on_delete=models.CASCADE,
                                 verbose_name='کامنت والد')
    rating = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.CharField(max_length=120)
    createdByBrowserName = models.CharField(max_length=120)
    createdByIp = models.CharField(max_length=120)
    status = models.CharField(max_length=255)
    isDelete = models.BooleanField(default=False, verbose_name='حذف شده / نشده')
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
