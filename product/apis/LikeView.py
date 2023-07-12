from rest_framework import status
from rest_framework.generics import RetrieveAPIView, UpdateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from product.serializers.LikeSerializer import LikeCreateSerializer

from helper.response import local_response, validation_response


class LikeCreateView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LikeCreateSerializer

    def post(self, request):
        request.data['userId'] = request.user.id
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return local_response('create', True, "ok", '', serializer.data)
        else:
            return validation_response(serializer.errors)
