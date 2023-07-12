from rest_framework import serializers, validators

from vendor.models import City


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'


class CityShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'title']


class CityCreateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100, error_messages={"required": "فیلد عنوان نمیتواند خالی باشد"})

    def create(self, validated_data):
        return City.objects.create(**validated_data)


class CityDeleteSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    isDelete = serializers.BooleanField(default=False)

    class Meta:
        model = City
        fields = ['id', 'isDelete']

    def validate_id(self, value):
        try:
            brand = City.objects.get(id=value)
        except City.DoesNotExist:
            raise serializers.ValidationError('City not found')
        return value
