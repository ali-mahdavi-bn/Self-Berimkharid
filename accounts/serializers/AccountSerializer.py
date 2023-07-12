from rest_framework import serializers

from accounts.models import User
from upload.models import Upload
from upload.serializers.UploadSerializer import UploadGetLinkSerializer


class BrandSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
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
