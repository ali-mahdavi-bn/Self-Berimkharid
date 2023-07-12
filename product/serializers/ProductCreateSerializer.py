from rest_framework import serializers

from product.models import Product


class ProductCreateSerializer(serializers.ModelSerializer):
    brandId = serializers.IntegerField(required=True)
    slug = serializers.CharField(required=True)
    shortDescription = serializers.CharField(required=True)

    class Meta:
        model = Product
        fields = (
            'name', 'slug', 'categoryId', 'brandId', 'uploadId', 'isUsed', 'shortDescription', 'status', 'description')

    def validate(self, data):
        if data['name'] == '':
            raise serializers.ValidationError('Product name cannot be empty')
        return data
