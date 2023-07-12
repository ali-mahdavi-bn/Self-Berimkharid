from django.db.models import Q
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from ..models import Vendor
from vendor.serializers.VendorSerializer import VendorCreateSerializer, VendorViewSerializer
from helper.response import local_response, validation_response


class VendorCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = VendorCreateSerializer

    def post(self, request):
        request.data['ownerId'] = request.user.id
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return local_response('create', True, "ok", '', serializer.data)
        else:
            return validation_response(serializer.errors)


class VendorListAPIView(APIView):
    serializer_class = VendorViewSerializer
    pagination_class = PageNumberPagination
    pagination_class.page_size = 10

    def get(self, request):
        vendors = Vendor.objects.filter( isDelete=False)
        city_id = request.query_params.get('cityId', None)

        if city_id:
            vendors = vendors.filter(categoryId=city_id)


        # Apply pagination
        paginator = self.pagination_class()
        paginated_products = paginator.paginate_queryset(vendors, request, view=self)

        serializer = self.serializer_class(paginated_products, many=True)
        return local_response('create', True, "ok", '', paginator.get_paginated_response(serializer.data).data)


class VendorDetailAPIView(APIView):
    serializer_class = VendorViewSerializer

    def get(self, request, id_or_slug):
        try:
            if id_or_slug.isdigit():
                vendor = Vendor.objects.get(
                    Q(id=id_or_slug),
                    isDelete=False
                )
            else:
                vendor = Vendor.objects.get(
                    Q(slug=id_or_slug),
                    isDelete=False
                )
            serializer = VendorViewSerializer(vendor)
            return local_response('create', True, "ok", '', serializer.data)
        except Vendor.DoesNotExist:
            # Handle the case where the product does not exist
            return local_response('notFound', True, "Vendor not found", '', None)
