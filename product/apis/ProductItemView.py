from rest_framework import status
from rest_framework.generics import RetrieveAPIView, UpdateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from product.models import Category
from product.serializers.CategorySerializer import CategorySerializer, CategoryViewSerializer, CategoryDeleteSerializer, \
    CategoryCreateSerializer, TreeCategorySerializer

from helper.response import local_response, validation_response


class ProductItemView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CategoryCreateSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # result = UploadShowSerializer(serializer.save())
            return local_response('create', True, "ok", '', serializer.data)
        else:
            return validation_response(serializer.errors)
