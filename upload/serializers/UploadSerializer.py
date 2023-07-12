from rest_framework import serializers, validators

from upload.models import Upload

import imghdr

from Berimkharid.local_settings import minioAddress

from helper.minio import upload_image_to_minio


class UploadGetLinkSerializer(serializers.ModelSerializer):
    link = serializers.SerializerMethodField()

    class Meta:
        model = Upload
        fields = ['link']

    def get_link(self, obj):
        return f'{minioAddress}/{obj.bucketName}/{obj.path}'


class UploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Upload
        fields = '__all__'


class UploadShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Upload
        fields = ['id', 'type', 'bucketName', 'path', 'createdAt']


class UploadCreateSerializer(serializers.Serializer):
    type = serializers.CharField(max_length=100, error_messages={"required": "فیلد تایپ نمیتواند خالی باشد"})
    file = serializers.FileField(error_messages={"required": "فیلد فایل نمیتواند خالی باشد"})

    def validate(self, data):
        if data['type'] != 'product' and data['type'] != 'userImage' and data['type'] != 'brand' \
                and data['type'] != 'category' and data['type'] != 'vendor' and data['type'] != 'eNamad':
            raise serializers.ValidationError({'type': ['اطلاعات وارد شده برای فیلد تایپ اشتباه است']})
        if data['file'].content_type not in ['image/jpeg', 'image/png', 'image/jpg']:
            raise serializers.ValidationError({'file': ['فرمت وارد شده برای فیلد فایل اشتباه است']})
        image_data = data['file'].read()
        image_format = imghdr.what(None, h=image_data)
        length = data['file'].size
        resultUpload = upload_image_to_minio(image_data, data['type'], image_format, length)
        if not resultUpload:
            raise serializers.ValidationError(
                {'file': [' خطایی در سرویس اپلود به وجود امده است لطفا مجدد تلاش کنید یا با پشتیبانی تماس بگیرید']})
        data['bucketName'] = resultUpload['bucketName']
        data['path'] = resultUpload['path']
        return data

    def create(self, validated_data):

        validated_data.pop('file', None)
        return Upload.objects.create(**validated_data)
