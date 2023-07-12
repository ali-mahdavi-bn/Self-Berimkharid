from rest_framework import serializers
import random

from accounts.models import User, UserDetails, VerifyUser
from helper.sendSms import sendSms
from helper.response import local_response, validation_response

#
from datetime import datetime, timedelta


class SellerShowInVendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'userName', 'firstName', 'lastName', 'email', 'phoneNumber']


class SellerSendCodeSerializer(serializers.Serializer):
    phoneNumber = serializers.CharField(max_length=120,
                                        error_messages={"required": "فیلد شماره تلفن نمیتواند خالی باشد"})

    def validate(self, data):
        mode = 'register'
        code = random.randrange(10000, 100000)
        checkUser = User.objects.filter(phoneNumber=data['phoneNumber'], type='seller').exists()
        if checkUser:
            mode = 'forgotPassword'
        checkSendSms = sendSms({'phoneNumber': data['phoneNumber'], 'code': code}, 'customerRegister')
        if checkSendSms:
            data['code'] = code
            data['mode'] = mode
        else:
            raise serializers.ValidationError(
                {'phoneNumber': ['خطایی در سرویس ارسال اس ام اس به وجود امده است لطفا با پشتیبانی تماس بگیرید']})
        return data

    def create(self, validated_data):
        return VerifyUser.objects.create(**validated_data)


class SellerRegisterSerializer(serializers.Serializer):
    phoneNumber = serializers.CharField(max_length=120,
                                        error_messages={"required": "فیلد شماره تلفن نمیتواند خالی باشد"})
    code = serializers.CharField(max_length=120,
                                 error_messages={"required": "فیلد کد نمیتواند خالی باشد"})
    userName = serializers.CharField(max_length=300,
                                     error_messages={"required": "فیلد نام کاربری  نمیتواند خالی باشد",
                                                     "unique": 'فیلد وارد شده برای نام کاربری اشتباه است'})
    firstName = serializers.CharField(max_length=120,
                                      error_messages={"required": "فیلد نام نمیتواند خالی باشد"})
    email = serializers.CharField(max_length=120,
                                  error_messages={"required": "فیلد ایمیل نمیتواند خالی باشد"})
    lastName = serializers.CharField(max_length=120,
                                     error_messages={"required": "فیلد نام خانوادگی نمیتواند خالی باشد"})
    password = serializers.CharField(max_length=120,
                                     error_messages={"required": "فیلد پسورد  نمیتواند خالی باشد"})
    nationalCode = serializers.CharField(max_length=120,
                                         error_messages={"required": "فیلد کد ملی  نمیتواند خالی باشد"})
    gender = serializers.CharField(max_length=120,
                                   error_messages={"required": "فیلد جنسیت  نمیتواند خالی باشد"})

    def validate(self, data):
        currentTime = datetime.now()
        startTime = currentTime - timedelta(minutes=5)
        try:
            checkCode = VerifyUser.objects.filter(phoneNumber=data['phoneNumber'], code=data['code'], isUsed=False,
                                                  mode='register')
        except VerifyUser.DoesNotExist:
            raise serializers.ValidationError({'code': ['کد وارد شده اشتباه است']})
        if data['gender'] == 'man' or data['gender'] == 'woman':
            raise serializers.ValidationError({'gender': ['فیلد وارد شده برای جنسیت اشتباه است']})
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
            lastName=validated_data['lastName'],
            phoneNumber=validated_data['phoneNumber'],
            email=validated_data['email'],
            type='seller',
            status='active'
        )
        user.set_password(validated_data['password'])
        user.save()
        print(user)
        print(validated_data['nationalCode'])
        print(validated_data['gender'])

        UserDetails.objects.create(
            userId=user,
            nationalCode=validated_data['nationalCode'],
            gender=validated_data['gender']
        )
        return user


class SellerLoginSerializer(serializers.Serializer):
    userName = serializers.CharField(max_length=300,
                                     error_messages={"required": "فیلد نام کاربری  نمیتواند خالی باشد",
                                                     "unique": 'فیلد وارد شده برای نام کاربری اشتباه است'})
    password = serializers.CharField(max_length=120,
                                     error_messages={"required": "فیلد پسورد  نمیتواند خالی باشد"})


class SellerForgotPasswordSerializer(serializers.Serializer):
    phoneNumber = serializers.CharField(max_length=120,
                                        error_messages={"required": "فیلد شماره تلفن نمیتواند خالی باشد"})
    code = serializers.CharField(max_length=120,
                                 error_messages={"required": "فیلد کد نمیتواند خالی باشد"})
    newPassword = serializers.CharField(max_length=120,
                                        error_messages={"required": "فیلد پسورد  نمیتواند خالی باشد"})
