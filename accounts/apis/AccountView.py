from rest_framework import status
from rest_framework.generics import RetrieveAPIView, UpdateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import Throttled
from rest_framework.permissions import IsAuthenticated

from accounts.models import User, VerifyUser
from accounts.serializers.CustomerSerializer import CustomerSendCodeSerializer, CustomerRegisterSerializer, \
    CustomerLoginWithPasswordSerializer, CustomerLoginWithCodeSerializer

from helper.response import local_response, validation_response
from helper.sendSms import sendSms
from helper.createToken import get_tokens_for_user
from helper.throttle import UserLoginRateThrottle


class AccountInfoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, ):
        return local_response('found', True, "ok", '', {'id': request.user.id, 'firstName': request.user.firstName,
                                                        'lastName': request.user.lastName, 'type': request.user.type, })
