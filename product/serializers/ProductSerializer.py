from rest_framework import serializers

from product.models import Product, Category, Brand, ProductItem, Like, FavoriteProduct
from product.serializers.BrandSerializer import BrandSerializer
from product.serializers.CategorySerializer import CategorySerializer, TreeCategorySerializer
from upload.serializers.UploadSerializer import UploadSerializer, UploadGetLinkSerializer
from upload.models import Upload
from accounts.models import User

from vendor.models import Vendor
import json
from django.db.models import Count
from django.db.models import Min, Max
from django.db.models.functions import Extract
from django.db.models import Subquery, OuterRef
from django.db.models.functions import RowNumber


class ProductViewSerializer(serializers.ModelSerializer):
    pictureGallery = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    brand = serializers.SerializerMethodField()
    prices = serializers.SerializerMethodField()
    isLike = serializers.SerializerMethodField()
    isFavorite = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'nameEn', 'prices', 'slug', 'metaTitle', 'isLike', 'details', 'isFavorite',
                  'metaDescription',
                  'description',
                  'shortDescription',
                  'metaKeywords', 'metaTitle', 'pictureGallery', 'category', 'brand', 'isUsed', 'showOnHomepage']

    def get_prices(self, obj):
        last_prices = ProductItem.objects.filter(productId=obj.id, inStock=True).values('vendorId').annotate(
            max_recordedAt=Max('recordedAt')).values('vendorId', 'price').order_by('vendorId')
        minPrice = None
        maxPrice = None
        if len(last_prices) > 0:
            vendor_prices = {}
            for price in last_prices:
                vendor_id = price['vendorId']
                vendor_price = price['price']
                vendor_prices[vendor_id] = vendor_price
            minPrice = min(vendor_prices.values())
            maxPrice = max(vendor_prices.values())

        return {'minPrice': minPrice, 'maxPrice': maxPrice}

    def get_category(self, obj):
        getCategory = TreeCategorySerializer(obj.categoryId)
        return getCategory.data

    def get_brand(self, obj):
        getBrand = BrandSerializer(obj.brandId)
        return getBrand.data

    def get_pictureGallery(self, obj):
        getPictureGallery = UploadGetLinkSerializer(obj.pictureGallery, many=True)
        pictureGalleryArray = []
        for pictureGallery in getPictureGallery.data:
            pictureGalleryArray.append(pictureGallery['link'])

        return pictureGalleryArray

    def get_isLike(self, obj):
        return False

    def get_isFavorite(self, obj):
        return False


class ProductViewWithUserSerializer(serializers.ModelSerializer):
    pictureGallery = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    brand = serializers.SerializerMethodField()
    prices = serializers.SerializerMethodField()
    isLike = serializers.SerializerMethodField()
    isFavorite = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'nameEn', 'prices', 'slug', 'metaTitle', 'isLike', 'isFavorite', 'details',
                  'metaDescription',
                  'description',
                  'shortDescription',
                  'metaKeywords', 'metaTitle', 'pictureGallery', 'category', 'brand', 'isUsed', 'showOnHomepage']

    def get_prices(self, obj):
        last_prices = ProductItem.objects.filter(productId=obj.id, inStock=True).values('vendorId').annotate(
            max_recordedAt=Max('recordedAt')).values('vendorId', 'price').order_by('vendorId')
        minPrice = None
        maxPrice = None
        if len(last_prices) > 0:
            vendor_prices = {}
            for price in last_prices:
                vendor_id = price['vendorId']
                vendor_price = price['price']
                vendor_prices[vendor_id] = vendor_price
            minPrice = min(vendor_prices.values())
            maxPrice = max(vendor_prices.values())

        return {'minPrice': minPrice, 'maxPrice': maxPrice}

    def get_category(self, obj):
        getCategory = TreeCategorySerializer(obj.categoryId)
        return getCategory.data

    def get_brand(self, obj):
        getBrand = BrandSerializer(obj.brandId)
        return getBrand.data

    def get_pictureGallery(self, obj):
        getPictureGallery = UploadGetLinkSerializer(obj.pictureGallery, many=True)
        pictureGalleryArray = []
        for pictureGallery in getPictureGallery.data:
            pictureGalleryArray.append(pictureGallery['link'])
        return pictureGalleryArray

    def get_isLike(self, obj):
        checkLike = Like.objects.filter(productId=obj.id, userId=self.context['userId']).exists()
        if checkLike:
            return True
        return False

    def get_isFavorite(self, obj):
        checkFavoriteProduct = FavoriteProduct.objects.filter(productId=obj.id, userId=self.context['userId']).exists()
        if checkFavoriteProduct:
            return True
        return False


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ProductCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=120, error_messages={"required": "فیلد  نام نمیتواند خالی باشد"})
    nameEn = serializers.CharField(max_length=300,
                                   error_messages={"required": "فیلد نام انگلیسی نمیتواند خالی باشد"})
    metaTitle = serializers.CharField(max_length=120, error_messages={"required": "فیلد عنوان متا نمیتواند خالی باشد"})
    metaKeywords = serializers.CharField(max_length=120,
                                         error_messages={"required": "فیلد کلید واژه های متا نمیتواند خالی باشد"})
    shortDescription = serializers.CharField(max_length=120,
                                             error_messages={"required": "فیلد توضیحات کوتاه نمیتواند خالی باشد"})
    description = serializers.CharField(max_length=120, error_messages={"required": "فیلد توضیحات نمیتواند خالی باشد"})
    metaDescription = serializers.CharField(max_length=120,
                                            error_messages={"required": "فیلد توضیحات متا نمیتواند خالی باشد"})
    slug = serializers.CharField(max_length=120,
                                 error_messages={"required": "فیلد  slug نمیتواند خالی باشد"})
    categoryId = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(),
                                                    error_messages={
                                                        "required": "فیلد ایدی دسته بندی نمیتواند خالی باشد",
                                                        "does_not_exist": " اطلاعات وارد شده برای فیلد ایدی دسته بندی اشتباه است "})
    brandId = serializers.PrimaryKeyRelatedField(queryset=Brand.objects.all(),
                                                 error_messages={
                                                     "required": "فیلد ایدی  برند نمیتواند خالی باشد",
                                                     "does_not_exist": " اطلاعات وارد شده برای فیلد ایدی برند  اشتباه است "})
    pictureGallery = serializers.PrimaryKeyRelatedField(queryset=Upload.objects.filter(type='product'), many=True)
    details = serializers.JSONField(error_messages={"required": "فیلد جزئیات نمیتواند خالی باشد",})

    def validate_details(self, value):
        try:
            # Attempt to parse the value as JSON
            details_string = json.dumps(value)
            json_data = json.loads(details_string)
        except json.JSONDecodeError:
            raise serializers.ValidationError({'slug': ['فرمت وارد شده برای فیلد جزئیان اشتباه است ']})

        # Additional validation logic for the JSON data if needed
        # ...

        return details_string

    def validate(self, data):
        checkSlug = Product.objects.filter(slug=data['slug']).exists()
        if checkSlug:
            raise serializers.ValidationError({'slug': ['فیلد وارد شده برای slug  تکراری است ']})
        return data

    def create(self, validated_data):
        product = Product.objects.create(
            name=validated_data['name'],
            nameEn=validated_data['nameEn'],
            metaTitle=validated_data['metaTitle'],
            metaKeywords=validated_data['metaKeywords'],
            shortDescription=validated_data['shortDescription'],
            description=validated_data['description'],
            metaDescription=validated_data['metaDescription'],
            slug=validated_data['slug'],
            categoryId=validated_data['categoryId'],
            brandId=validated_data['brandId'],
            details=validated_data['details']
        )
        product.pictureGallery.set(validated_data['pictureGallery'])
        product.save()
        return product


class ProductUpdateSerializer(serializers.Serializer):
    productIds = serializers.PrimaryKeyRelatedField(queryset=Product.objects.filter(), many=True, error_messages={
        "required": "فیلد ایدی  محصولات نمیتواند خالی باشد",
        "does_not_exist": " اطلاعات وارد شده برای فیلد ایدی محصولات  اشتباه است "})

    name = serializers.CharField(max_length=120, required=False, )
    nameEn = serializers.CharField(max_length=300, required=False, )
    metaTitle = serializers.CharField(max_length=120, required=False, )
    metaKeywords = serializers.CharField(max_length=120, required=False, )
    shortDescription = serializers.CharField(max_length=120, required=False)
    description = serializers.CharField(max_length=120, required=False)
    metaDescription = serializers.CharField(max_length=120, required=False, )
    status = serializers.CharField(max_length=120, required=False, )
    isUsed = serializers.BooleanField(required=False, )
    showOnHomepage = serializers.BooleanField(required=False, )
    isActive = serializers.BooleanField(required=False, )
    categoryId = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), required=False,
                                                    error_messages={
                                                        "does_not_exist": " اطلاعات وارد شده برای فیلد ایدی دسته بندی اشتباه است "})
    brandId = serializers.PrimaryKeyRelatedField(queryset=Brand.objects.all(), required=False,
                                                 error_messages={
                                                     "does_not_exist": " اطلاعات وارد شده برای فیلد ایدی برند  اشتباه است "})
    pictureGallery = serializers.PrimaryKeyRelatedField(required=False, queryset=Upload.objects.filter(),
                                                        many=True)
