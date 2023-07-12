from rest_framework import status
from rest_framework.generics import RetrieveAPIView, UpdateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from vendor.models import ClickHistory
from vendor.serializers.ClickHistorySerilalizer import ClickHistoryCreateSerializer

from helper.response import local_response, validation_response

import re
from user_agents import parse


class ClickHistoryCreateView(APIView):
    serializer_class = ClickHistoryCreateSerializer

    def get_ipv4_address(self, request):
        ip_address = request.META.get('REMOTE_ADDR')
        ipv4_match = re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', ip_address)
        if ipv4_match:
            return ip_address
        return None

    def get_ipv6_address(self, request):
        ip_address = request.META.get('REMOTE_ADDR')
        ipv6_match = re.match(
            r'^[0-9a-fA-F:]+:[0-9a-fA-F:]+:[0-9a-fA-F:]+:[0-9a-fA-F:]+$',
            ip_address
        )
        if ipv6_match:
            return ip_address
        return None

    def get_browser_name(self, user_agent):

        if 'Chrome' in user_agent:
            return 'Chrome'
        elif 'Firefox' in user_agent:
            return 'Firefox'
        if 'Internet' in user_agent:
            return 'Internet'
        elif 'Explorer' in user_agent:
            return 'Explorer'
        if 'Google' in user_agent:
            return 'Google'
        elif 'Mozilla' in user_agent:
            return 'Mozilla'
        if 'Safari' in user_agent:
            return 'Safari'
        elif 'Opera' in user_agent:
            return 'Opera'
        elif 'Konqueror' in user_agent:
            return 'Konqueror'
        elif 'Lynx' in user_agent:
            return 'Lynx'
        return 'Unknown'

    def post(self, request):
        ipAddress = request.META.get('REMOTE_ADDR')
        ipv4Address = self.get_ipv4_address(request)
        ipv6Address = self.get_ipv6_address(request,) or 'Unknown'
        userAgent = request.META.get('HTTP_USER_AGENT')
        browserName = self.get_browser_name(userAgent)
        userAgentParse = parse(userAgent)
        deviceName = userAgentParse.device.family
        deviceResolution = request.META.get('HTTP_X_DEVICE_RESOLUTION') or 'Unknown'
        sessionKey = f'{userAgent}{deviceName}{ipAddress}'
        #
        value = request.data.copy()
        value['ipv4'] = ipv4Address
        value['ipv6'] = ipv6Address
        value['userAgent'] = userAgent
        value['browserName'] = browserName
        value['deviceName'] = deviceName
        value['deviceResolution'] = deviceResolution
        value['sessionKey'] = sessionKey

        checkSessionKey = ClickHistory.objects.filter(sessionKey=sessionKey).exists()
        if checkSessionKey:
            return local_response('create', True, "ok", '', {})

        serializer = self.serializer_class(data=value)
        if serializer.is_valid():
            serializer.save()
            return local_response('create', True, "ok", '', {})
        else:
            return validation_response(serializer.errors)
