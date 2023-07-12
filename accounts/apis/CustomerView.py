from rest_framework import status
from rest_framework.generics import RetrieveAPIView, UpdateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import Throttled

from accounts.models import User, VerifyUser
from accounts.serializers.CustomerSerializer import CustomerSendCodeSerializer, CustomerRegisterSerializer, \
    CustomerLoginWithPasswordSerializer, CustomerLoginWithCodeSerializer

from helper.response import local_response, validation_response
from helper.sendSms import sendSms
from helper.createToken import get_tokens_for_user
from helper.throttle import UserLoginRateThrottle


class CustomerSendCodeView(APIView):
    serializer_class = CustomerSendCodeSerializer
    throttle_classes = (UserLoginRateThrottle,)

    # def throttled(self, request, wait):
    #     raise Throttled(detail={
    #         "message": "recaptcha_required",
    #     })

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return local_response('create', True, "ok", '', {'mode': serializer.validated_data['mode']})
        else:
            return validation_response(serializer.errors)


class CustomerRegisterView(APIView):
    serializer_class = CustomerRegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            result = serializer.save()
            token = get_tokens_for_user(result)
            return local_response('create', True, "ok", '', {'token': token})
        else:
            return validation_response(serializer.errors)


class CustomerLoginWithPasswordView(APIView):
    serializer_class = CustomerLoginWithPasswordSerializer

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            try:
                checkUser = User.objects.get(userName=data['userName'],
                                             type='customer')
            except User.DoesNotExist:
                return local_response('unAuthorized', False, "نام کاربری یا رمز عبور اشتباه است", '', '')

            if not checkUser.check_password(data['password']):
                return local_response('unAuthorized', False, "نام کاربری یا رمز عبور اشتباه است", '', '')
            token = get_tokens_for_user(checkUser)
            return local_response('create', True, "ok", '', {'token': token})
        else:
            return validation_response(serializer.errors)


class CustomerLoginWithCodeView(APIView):
    serializer_class = CustomerLoginWithCodeSerializer

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            try:
                VerifyUser.objects.get(phoneNumber=data['phoneNumber'], code=data['code'],
                                       mode='loginCustomer', isUsed=False)
            except VerifyUser.DoesNotExist:
                return local_response('unAuthorized', False, " اطلاعات وارد شده اشتباه است", '', {})
            try:
                checkUser = User.objects.get(phoneNumber=data['phoneNumber'], type='customer')
            except User.DoesNotExist:
                return local_response('serverErr', False,
                                      "خطایی رخ داده است مجددا تلاش کنید یا با پشتیبانی تماس بگیرید", '', '')
            token = get_tokens_for_user(checkUser)
            return local_response('create', True, "ok", '', {'token': token})
        else:
            return validation_response(serializer.errors)
