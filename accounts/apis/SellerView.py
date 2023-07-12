from rest_framework import status
from rest_framework.generics import RetrieveAPIView, UpdateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import User, VerifyUser
from accounts.serializers.SellerSerializer import SellerSendCodeSerializer, SellerRegisterSerializer, \
    SellerLoginSerializer, SellerForgotPasswordSerializer

from helper.response import local_response, validation_response
from helper.sendSms import sendSms
from helper.createToken import get_tokens_for_user


class SellerSendCodeView(APIView):
    serializer_class = SellerSendCodeSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return local_response('create', True, "ok", '', {'mode': serializer.validated_data['mode']})
        else:
            return validation_response(serializer.errors)


class SellerRegisterView(APIView):
    serializer_class = SellerRegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            result = serializer.save()
            token = get_tokens_for_user(result)
            return local_response('create', True, "ok", '', {'token': token})
        else:
            return validation_response(serializer.errors)


class SellerLoginView(APIView):
    serializer_class = SellerLoginSerializer

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            try:
                checkUser = User.objects.get(userName=data['userName'],
                                             type='seller')
            except User.DoesNotExist:
                return local_response('unAuthorized', False, "نام کاربری یا رمز عبور اشتباه است", '', '')

            if not checkUser.check_password(data['password']):
                return local_response('unAuthorized', False, "نام کاربری یا رمز عبور اشتباه است", '', '')
            token = get_tokens_for_user(checkUser)
            return local_response('create', True, "ok", '', {'token': token})
        else:
            return validation_response(serializer.errors)


class SellerRestPasswordView(APIView):
    serializer_class = SellerForgotPasswordSerializer

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            try:
                VerifyUser.objects.get(phoneNumber=data['phoneNumber'], code=data['code'],
                                       mode='customerForgotPassword', isUsed=False)
            except VerifyUser.DoesNotExist:
                return local_response('unAuthorized', False, " اطلاعات وارد شده اشتباه است", '', {})
            try:
                checkUser = User.objects.get(phoneNumber=data['phoneNumber'], type='seller')
            except User.DoesNotExist:
                return local_response('serverErr', False, "خطایی رخ داده است مجددا تلاش کنید یا با پشتیبانی تماس بگیرید", '', '')

            checkUser.set_password(data['newPassword'])
            checkUser.save()
            token = get_tokens_for_user(checkUser)
            return local_response('create', True, "ok", '', {'token': token})
        else:
            return validation_response(serializer.errors)
