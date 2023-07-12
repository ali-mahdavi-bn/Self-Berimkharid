from rest_framework import serializers
import random

from accounts.models import User, UserDetails, VerifyUser
from helper.sendSms import sendSms
from helper.response import local_response, validation_response

#
from datetime import datetime, timedelta


class VerifyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = VerifyUser
        fields = '__all__'


class CustomerSendCodeSerializer(serializers.Serializer):
    phoneNumber = serializers.CharField(max_length=120,
                                        error_messages={"required": "فیلد شماره تلفن نمیتواند خالی باشد"})

    def validate(self, data):
        mode = 'loginRegister'
        code = random.randrange(10000, 100000)
        checkUser = User.objects.filter(phoneNumber=data['phoneNumber'], type='customer').exists()
        if checkUser:
            mode = 'loginCustomer'
        checkSendSms = sendSms({'phoneNumber':data['phoneNumber'],'code':code}, 'customerRegister')
        if checkSendSms:
            data['code'] = code
            data['mode'] = mode
        else:
            raise serializers.ValidationError(
                {'phoneNumber': ['خطایی در سرویس ارسال اس ام اس به وجود امده است لطفا با پشتیبانی تماس بگیرید']})
        return data

    def create(self, validated_data):
        return VerifyUser.objects.create(**validated_data)


class CustomerRegisterSerializer(serializers.Serializer):
    phoneNumber = serializers.CharField(max_length=120,
                                        error_messages={"required": "فیلد شماره تلفن نمیتواند خالی باشد"})
    code = serializers.CharField(max_length=120,
                                 error_messages={"required": "فیلد کد نمیتواند خالی باشد"})
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
        currentTime = datetime.now()
        startTime = currentTime - timedelta(minutes=5)
        try:
            checkCode = VerifyUser.objects.filter(phoneNumber=data['phoneNumber'], code=data['code'], isUsed=False,
                                                  mode='loginRegister')
        except VerifyUser.DoesNotExist:
            raise serializers.ValidationError({'code': ['کد وارد شده اشتباه است']})
        checkUserName = User.objects.filter(userName=data['userName']).exists()
        if checkUserName:
            raise serializers.ValidationError({'userName': ['فیلد وارد شده برای نام کاربری تکراری است ']})
        # updateVerifyUser = VerifyUserSerializer(checkCode, data={'isUsed': True})
        # if updateVerifyUser.is_valid():
        #     updateVerifyUser.save()
        # else:
        #     raise serializers.ValidationError(
        #         ' خطایی پیش امده است لطفا دوباره تلاش کنید یا با پشتیبانی تماس بگیرید')

        return data

    def create(self, validated_data):
        user = User.objects.create(
            userName=validated_data['userName'],
            firstName=validated_data['firstName'],
            lastName=validated_data['lastName'],
            phoneNumber=validated_data['phoneNumber'],
            type='customer',
            status='active'
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class CustomerLoginWithPasswordSerializer(serializers.Serializer):
    userName = serializers.CharField(max_length=300,
                                     error_messages={"required": "فیلد نام کاربری  نمیتواند خالی باشد",
                                                     "unique": 'فیلد وارد شده برای نام کاربری اشتباه است'})
    password = serializers.CharField(max_length=120,
                                     error_messages={"required": "فیلد پسورد  نمیتواند خالی باشد"})


class CustomerLoginWithCodeSerializer(serializers.Serializer):
    phoneNumber = serializers.CharField(max_length=120,
                                        error_messages={"required": "فیلد شماره تلفن نمیتواند خالی باشد"})
    code = serializers.CharField(max_length=120,
                                 error_messages={"required": "فیلد کد نمیتواند خالی باشد"})

