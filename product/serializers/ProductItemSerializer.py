from rest_framework import serializers

from product.models import ProductItem


class BrandCreateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=120, error_messages={"required": "فیلد عنوان نمیتواند خالی باشد"})
    titleEn = serializers.CharField(max_length=300,
                                    error_messages={"required": "فیلد عنوان انگلیسی نمیتواند خالی باشد"})
    metaTitle = serializers.CharField(max_length=120, error_messages={"required": "فیلد عنوان متا نمیتواند خالی باشد"})
    metaKeywords = serializers.CharField(max_length=120,
                                         error_messages={"required": "فیلد کلید واژه های متا نمیتواند خالی باشد"})
    description = serializers.CharField(max_length=120, error_messages={"required": "فیلد توضیحات نمیتواند خالی باشد"})
    metaDescription = serializers.CharField(max_length=120,
                                            error_messages={"required": "فیلد توضیحات متا نمیتواند خالی باشد"})
    slug = serializers.CharField(max_length=120,
                                 error_messages={"required": "فیلد  slug نمیتواند خالی باشد"})

    pictureId = serializers.PrimaryKeyRelatedField(queryset=Upload.objects.filter(type='brand'),
                                                   error_messages={"required": "فیلد ایدی عکس نمیتواند خالی باشد",
                                                                   "does_not_exist": " اطلاعات وارد شده برای فیلد ایدی عکس اشتباه است "})
    iconId = serializers.PrimaryKeyRelatedField(queryset=Upload.objects.filter(type='brand'),
                                                error_messages={"required": "فیلد ایدی ایکون نمیتواند خالی باشد",
                                                                "does_not_exist": " اطلاعات وارد شده برای فیلد ایدی ایکون اشتباه است "})

    # def validate(self, data):
    #     checkSlug = Brand.objects.filter(slug=data['slug']).exists()
    #     if checkSlug:
    #         raise serializers.ValidationError({'slug': ['فیلد وارد شده برای slug  تکراری است ']})
    #     return data

    def create(self, validated_data):
        return ProductItem.objects.create(**validated_data)