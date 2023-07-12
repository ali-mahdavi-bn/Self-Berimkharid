from rest_framework import serializers

from product.models import Product, Category, Brand
from vendor.models import Vendor, City
from product.serializers.BrandSerializer import BrandSerializer
from product.serializers.CategorySerializer import CategorySerializer, TreeCategorySerializer
from upload.serializers.UploadSerializer import UploadSerializer, UploadGetLinkSerializer
from product.models import Product, Like
from accounts.models import User
from vendor.serializers.CitySerializer import CityShowSerializer
from accounts.serializers.SellerSerializer import SellerShowInVendorSerializer


class LikeCreateSerializer(serializers.Serializer):
    productId = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(),
                                                   error_messages={
                                                       "required": "فیلد ایدی محصول  نمیتواند خالی باشد",
                                                       "does_not_exist": " اطلاعات وارد شده برای فیلد ایدی محصول  اشتباه است "})
    userId = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(type='customer'))

    def create(self, validated_data):
        like = Like.objects.create(
            productId=validated_data['productId'],
            userId=validated_data['userId'],
        )
        return like
