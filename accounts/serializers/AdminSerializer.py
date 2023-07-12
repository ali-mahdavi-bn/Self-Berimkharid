from rest_framework import serializers

from accounts.models import User, UserDetails, VerifyUser


class AdminLoginWithPasswordSerializer(serializers.Serializer):
    userName = serializers.CharField(max_length=300,
                                     error_messages={"required": "فیلد نام کاربری  نمیتواند خالی باشد",
                                                     "unique": 'فیلد وارد شده برای نام کاربری اشتباه است'})
    password = serializers.CharField(max_length=120,
                                     error_messages={"required": "فیلد پسورد  نمیتواند خالی باشد"})


class AdminRegisterSerializer(serializers.Serializer):
    phoneNumber = serializers.CharField(max_length=120,
                                        error_messages={"required": "فیلد شماره تلفن نمیتواند خالی باشد"})
    email = serializers.CharField(max_length=120,
                                  error_messages={"required": "فیلد ایمیل نمیتواند خالی باشد"})
    userName = serializers.CharField(max_length=300,
                                     error_messages={"required": "فیلد نام کاربری  نمیتواند خالی باشد",
                                                     "unique": 'فیلد وارد شده برای نام کاربری اشتباه است'})
    firstName = serializers.CharField(max_length=120,
                                      error_messages={"required": "فیلد نام نمیتواند خالی باشد"})
    lastName = serializers.CharField(max_length=120,
                                     error_messages={"required": "فیلد نام خانوادگی نمیتواند خالی باشد"})
    password = serializers.CharField(max_length=120,
                                     error_messages={"required": "فیلد پسورد  نمیتواند خالی باشد"})

    def validate(self, data):
        checkUserName = User.objects.filter(userName=data['userName']).exists()
        if checkUserName:
            raise serializers.ValidationError({'userName': ['فیلد وارد شده برای نام کاربری تکراری است ']})
        checkPhoneNumber = User.objects.filter(phoneNumber=data['phoneNumber']).exists()
        if checkPhoneNumber:
            raise serializers.ValidationError({'phoneNumber': ['شماره همراه وارد شده تکراری است']})
        checkEmail = User.objects.filter(email=data['email']).exists()
        if checkEmail:
            raise serializers.ValidationError({'email': ['ایمیل  وارد شده تکراری است']})
        return data

    def create(self, validated_data):
        user = User.objects.create(
            userName=validated_data['userName'],
            firstName=validated_data['firstName'],
            email=validated_data['email'],
            lastName=validated_data['lastName'],
            phoneNumber=validated_data['phoneNumber'],
            type='admin',
            status='active'
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
