from rest_framework import serializers

from product.models import Brand
from upload.models import Upload
from upload.serializers.UploadSerializer import UploadGetLinkSerializer


class BrandSerializer(serializers.ModelSerializer):
    isActive = serializers.BooleanField(default=True, write_only=True)
    isDelete = serializers.BooleanField(default=False, write_only=True)
    icon = serializers.SerializerMethodField()
    picture = serializers.SerializerMethodField()

    class Meta:
        model = Brand
        fields = ['id', 'title', 'titleEn', 'slug', 'metaTitle', 'picture','internal', 'metaDescription', 'description',
                  'metaKeywords', 'metaTitle', 'icon', 'isActive', 'isDelete']

    def get_picture(self, obj):
        pictureLink = UploadGetLinkSerializer(obj.pictureId)
        return pictureLink.data['link']
    def get_icon(self, obj):
        iconLink = UploadGetLinkSerializer(obj.iconId)
        return iconLink.data['link']
    def create(self, validated_data):
        validated_data['isActive'] = self.initial_data.get('isActive', True)
        validated_data['isDelete'] = self.initial_data.get('isDelete', False)
        instance = super().create(validated_data)
        return instance

    def validate(self, data):
        """
        Check that only one of is_active and is_delete is True
        """
        is_active = data.get('isActive')
        is_delete = data.get('isDelete')
        if is_active and is_delete:
            raise serializers.ValidationError("Only one of is_active and is_delete can be True")
        if not is_active and not is_delete:
            raise serializers.ValidationError("At least one of is_active and is_delete must be True")
        return data


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
    internal = serializers.BooleanField(error_messages={"required": "وارد کردن فیلد داخلی یا خارجی الزامی است"})

    pictureId = serializers.PrimaryKeyRelatedField(queryset=Upload.objects.filter(type='brand'),
                                                   error_messages={"required": "فیلد ایدی عکس نمیتواند خالی باشد",
                                                                   "does_not_exist": " اطلاعات وارد شده برای فیلد ایدی عکس اشتباه است "})
    iconId = serializers.PrimaryKeyRelatedField(queryset=Upload.objects.filter(type='brand'),
                                                error_messages={"required": "فیلد ایدی ایکون نمیتواند خالی باشد",
                                                                "does_not_exist": " اطلاعات وارد شده برای فیلد ایدی ایکون اشتباه است "})

    def validate(self, data):
        checkSlug = Brand.objects.filter(slug=data['slug']).exists()
        if checkSlug:
            raise serializers.ValidationError({'slug': ['فیلد وارد شده برای slug  تکراری است ']})
        return data

    def create(self, validated_data):
        return Brand.objects.create(**validated_data)


class BrandDeleteSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    isDelete = serializers.BooleanField(default=False)

    class Meta:
        model = Brand
        fields = ['id', 'isDelete']

    def validate_id(self, value):
        try:
            brand = Brand.objects.get(id=value)
        except Brand.DoesNotExist:
            raise serializers.ValidationError('Brand not found')
        return value
