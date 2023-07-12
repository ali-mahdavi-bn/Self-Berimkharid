from rest_framework import serializers

from product.models import Product


class ProductUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    # def validate(self, data):
    #     if data['name'] == '':
    #         raise serializers.ValidationError('Product name cannot be empty')
    #     return data
