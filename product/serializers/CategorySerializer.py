from rest_framework import serializers

from product.models import Category
from upload.models import Upload
from upload.serializers.UploadSerializer import UploadGetLinkSerializer


class CategoryViewSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    picture = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('id', 'title', 'titleEn', 'slug', 'children', 'metaTitle', 'picture', 'metaDescription',
                  'description', 'metaKeywords', 'metaTitle',
                   'isActive',
                  'isDelete')

    def get_picture(self, obj):
        pictureLink = UploadGetLinkSerializer(obj.pictureId)
        return pictureLink.data['link']
    def get_children(self, obj):
        serializer = CategoryViewSerializer(obj.category_parent.all(), many=True)
        return serializer.data


class TreeCategorySerializer(serializers.ModelSerializer):
    parent = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('id', 'title', 'titleEn', 'slug', 'parent', 'metaTitle', 'metaDescription',
                  'description', 'metaKeywords', 'metaTitle',
                   'isActive',
                  'isDelete')

    def get_parent(self, obj):
        if obj.parentId:
            parent = Category.objects.get(id=obj.parentId.id)
            serializer = TreeCategorySerializer(parent)
            return serializer.data
        else:
            return None
class CategorySerializer(serializers.ModelSerializer):
    isActive = serializers.BooleanField(default=True, write_only=True)
    isDelete = serializers.BooleanField(default=False, write_only=True)
    pictureId = UploadGetLinkSerializer()

    # parentId= CategorySerializer()

    class Meta:
        model = Category
        fields = ['id', 'title', 'titleEn', 'slug', 'parentId', 'metaTitle', 'pictureId', 'metaDescription',
                  'description', 'metaKeywords', 'metaTitle',
                  'isPublished', 'isActive',
                  'isDelete']

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


class CategoryCreateSerializer(serializers.Serializer):
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
    pictureId = serializers.PrimaryKeyRelatedField(queryset=Upload.objects.filter(type='category'),
                                                   error_messages={"required": "فیلد ایدی عکس نمیتواند خالی باشد",
                                                                   "does_not_exist": " اطلاعات وارد شده برای فیلد ایدی عکس اشتباه است "})
    parentId = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(),required=False)

    def validate(self, data):
        checkSlug = Category.objects.filter(slug=data['slug']).exists()
        if checkSlug:
            raise serializers.ValidationError({'slug': ['فیلد وارد شده برای slug  تکراری است ']})
        if 'parentId' in data:
            checkParentId = Category.objects.filter(id=data['parentId'].id).exists()
            if not checkParentId:
                raise serializers.ValidationError({'parentId': ['اطلاعات وارد شده برای فیلد ایدی والد اشتباه است ']})
        return data

    def create(self, validated_data):
        if 'parentId' in validated_data:
            return Category.objects.create(
                title=validated_data['title'],
                titleEn=validated_data['titleEn'],
                metaTitle=validated_data['metaTitle'],
                metaKeywords=validated_data['metaKeywords'],
                description=validated_data['description'],
                metaDescription=validated_data['metaDescription'],
                slug=validated_data['slug'],
                pictureId=validated_data['pictureId'],
                parentId=validated_data['parentId'],
            )
        else:
            return Category.objects.create(
                title=validated_data['title'],
                titleEn=validated_data['titleEn'],
                metaTitle=validated_data['metaTitle'],
                metaKeywords=validated_data['metaKeywords'],
                description=validated_data['description'],
                metaDescription=validated_data['metaDescription'],
                slug=validated_data['slug'],
                pictureId=validated_data['pictureId'],
            )


class CategoryDeleteSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    isDelete = serializers.BooleanField(default=False)

    class Meta:
        model = Category
        fields = ['id', 'isDelete']

    def validate_id(self, value):
        try:
            category = Category.objects.get(id=value)
        except Category.DoesNotExist:
            raise serializers.ValidationError('Category not found')
        return value
