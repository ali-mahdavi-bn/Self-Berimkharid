from rest_framework import status
from rest_framework.generics import RetrieveAPIView, UpdateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import User, VerifyUser
from accounts.serializers.AdminSerializer import AdminLoginWithPasswordSerializer,AdminRegisterSerializer

from helper.response import local_response, validation_response
from helper.sendSms import sendSms
from helper.createToken import get_tokens_for_user

class AdminRegisterView(APIView):
    serializer_class = AdminRegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            result = serializer.save()
            token = get_tokens_for_user(result)
            return local_response('create', True, "ok", '', {'token': token})
        else:
            return validation_response(serializer.errors)
class AdminLoginWithPasswordView(APIView):
    serializer_class = AdminLoginWithPasswordSerializer

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            try:
                checkUser = User.objects.get(userName=data['userName'],
                                             type='admin')
            except User.DoesNotExist:
                return local_response('unAuthorized', False, "نام کاربری یا رمز عبور اشتباه است", '', '')

            if not checkUser.check_password(data['password']):
                return local_response('unAuthorized', False, "نام کاربری یا رمز عبور اشتباه است", '', '')
            token = get_tokens_for_user(checkUser)
            return local_response('create', True, "ok", '', {'token': token})
        else:
            return validation_response(serializer.errors)
