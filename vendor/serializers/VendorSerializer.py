from rest_framework import serializers

from product.models import Product, Category, Brand
from vendor.models import Vendor, City
from product.serializers.BrandSerializer import BrandSerializer
from product.serializers.CategorySerializer import CategorySerializer, TreeCategorySerializer
from upload.serializers.UploadSerializer import UploadSerializer, UploadGetLinkSerializer
from upload.models import Upload
from accounts.models import User
from vendor.serializers.CitySerializer import CityShowSerializer
from accounts.serializers.SellerSerializer import SellerShowInVendorSerializer


class VendorViewSerializer(serializers.ModelSerializer):
    pictureGallery = UploadGetLinkSerializer(many=True)
    iconId = UploadGetLinkSerializer()
    cityId = CityShowSerializer()
    ownerId = SellerShowInVendorSerializer()

    class Meta:
        model = Vendor
        fields = ['id', 'name', 'nameEn', 'slug', 'metaDescription', 'description',
                  'metaKeywords', 'metaName', 'pictureGallery', 'link', 'postingMethods', 'phoneNumber', 'address',
                  'latitude', 'longitude', 'zipCode', 'paymentMethods', 'orderTrackingMethods', 'cityId', 'iconId',
                  'ownerId']


class VendorCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=120, error_messages={"required": "فیلد  نام نمیتواند خالی باشد"})
    nameEn = serializers.CharField(max_length=300,
                                   error_messages={"required": "فیلد نام انگلیسی نمیتواند خالی باشد"})
    metaName = serializers.CharField(max_length=120, error_messages={"required": "فیلد عنوان متا نمیتواند خالی باشد"})
    metaKeywords = serializers.CharField(max_length=120,
                                         error_messages={"required": "فیلد کلید واژه های متا نمیتواند خالی باشد"})
    description = serializers.CharField(max_length=120, error_messages={"required": "فیلد توضیحات نمیتواند خالی باشد"})
    metaDescription = serializers.CharField(max_length=120,
                                            error_messages={"required": "فیلد توضیحات متا نمیتواند خالی باشد"})
    link = serializers.CharField(max_length=120,
                                 error_messages={"required": "فیلد  لینک سایت نمیتواند خالی باشد"})
    postingMethods = serializers.CharField(max_length=120,
                                           error_messages={"required": "فیلد  روش های ارسال  نمیتواند خالی باشد"})
    phoneNumber = serializers.CharField(max_length=120,
                                        error_messages={"required": "فیلد   شماره تماس   نمیتواند خالی باشد"})
    address = serializers.CharField(max_length=120,
                                    error_messages={"required": "فیلد   ادرس    نمیتواند خالی باشد"})
    latitude = serializers.CharField(max_length=120,
                                     error_messages={"required": "فیلد  طول جغرافیایی    نمیتواند خالی باشد"})
    longitude = serializers.CharField(max_length=120,
                                      error_messages={"required": "فیلد عرض جغرافیایی   نمیتواند خالی باشد"})
    zipCode = serializers.CharField(max_length=120,
                                    error_messages={"required": "فیلد کد پستی    نمیتواند خالی باشد"})
    paymentMethods = serializers.CharField(max_length=120,
                                           error_messages={"required": "فیلد روش های ارسال   نمیتواند خالی باشد"})
    orderTrackingMethods = serializers.CharField(max_length=120,
                                                 error_messages={
                                                     "required": "فیلد روش های پیگیری   نمیتواند خالی باشد"})
    slug = serializers.CharField(max_length=120,
                                 error_messages={"required": "فیلد  slug نمیتواند خالی باشد"})
    cityId = serializers.PrimaryKeyRelatedField(queryset=City.objects.all(),
                                                error_messages={
                                                    "required": "فیلد ایدی شهر  نمیتواند خالی باشد",
                                                    "does_not_exist": " اطلاعات وارد شده برای فیلد ایدی شهر  اشتباه است "})
    iconId = serializers.PrimaryKeyRelatedField(queryset=Upload.objects.filter(type='vendor'),
                                                error_messages={
                                                    "required": "فیلد ایدی  ایکون نمیتواند خالی باشد",
                                                    "does_not_exist": " اطلاعات وارد شده برای فیلد ایدی ایکون  اشتباه است "})
    pictureGallery = serializers.PrimaryKeyRelatedField(queryset=Upload.objects.filter(type='vendor'), many=True)
    ownerId = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    def validate(self, data):
        checkSlug = Vendor.objects.filter(slug=data['slug']).exists()
        if checkSlug:
            raise serializers.ValidationError({'slug': ['فیلد وارد شده برای slug  تکراری است ']})
        return data

    def create(self, validated_data):
        vendor = Vendor.objects.create(
            name=validated_data['name'],
            nameEn=validated_data['nameEn'],
            metaName=validated_data['metaName'],
            metaKeywords=validated_data['metaKeywords'],
            link=validated_data['link'],
            description=validated_data['description'],
            metaDescription=validated_data['metaDescription'],
            slug=validated_data['slug'],
            iconId=validated_data['iconId'],
            cityId=validated_data['cityId'],
            orderTrackingMethods=validated_data['orderTrackingMethods'],
            paymentMethods=validated_data['paymentMethods'],
            zipCode=validated_data['zipCode'],
            longitude=validated_data['longitude'],
            latitude=validated_data['latitude'],
            address=validated_data['address'],
            phoneNumber=validated_data['phoneNumber'],
            postingMethods=validated_data['postingMethods'],
            ownerId=validated_data['ownerId'],

        )
        vendor.pictureGallery.set(validated_data['pictureGallery'])
        vendor.save()
        return vendor
