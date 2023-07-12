from rest_framework import serializers, validators

from vendor.models import ClickHistory, Vendor
from product.models import Product


class ClickHistoryCreateSerializer(serializers.Serializer):
    productId = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(),
                                                   error_messages={
                                                       "required": "فیلد ایدی محصول  نمیتواند خالی باشد",
                                                       "does_not_exist": " اطلاعات وارد شده برای فیلد ایدی محصول  اشتباه است "})
    vendorId = serializers.PrimaryKeyRelatedField(queryset=Vendor.objects.all(),
                                                  error_messages={
                                                      "required": "فیلد ایدی فروشگاه  نمیتواند خالی باشد",
                                                      "does_not_exist": " اطلاعات وارد شده برای فیلد ایدی فروشگاه  اشتباه است "})
    userAgent = serializers.CharField(max_length=100, error_messages={"required": "فیلد مورد نظر نمیتواند خالی باشد"})
    ipv4 = serializers.CharField(max_length=100, error_messages={"required": "فیلد مورد نظر نمیتواند خالی باشد"})
    ipv6 = serializers.CharField(max_length=100, error_messages={"required": "فیلد مورد نظر نمیتواند خالی باشد"})
    browserName = serializers.CharField(max_length=100, error_messages={"required": "فیلد مورد نظر نمیتواند خالی باشد"})
    deviceName = serializers.CharField(max_length=100, error_messages={"required": "فیلد مورد نظر نمیتواند خالی باشد"})
    deviceResolution = serializers.CharField(max_length=100, error_messages={"required": "فیلد مورد نظر نمیتواند خالی باشد"})
    sessionKey = serializers.CharField(max_length=100, error_messages={"required": "فیلد مورد نظر نمیتواند خالی باشد"})

    def create(self, validated_data):
        return ClickHistory.objects.create(**validated_data)
