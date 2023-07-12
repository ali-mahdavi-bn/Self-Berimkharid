from django.db.models import Q
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from ..models import Product
# from ..serializers.ProductCreateSerializer import ProductCreateSerializer
# from ..serializers.ProductSerializer import ProductSerializer
# from ..serializers.ProductUpdateSerializer import ProductUpdateSerializer
from product.serializers.ProductSerializer import ProductSerializer, ProductCreateSerializer, ProductViewSerializer, \
    ProductUpdateSerializer, ProductViewWithUserSerializer
from helper.response import local_response, validation_response


class ProductListAPIView(APIView):
    pagination_class = PageNumberPagination
    pagination_class.page_size = 10

    def get(self, request):
        products = Product.objects.filter(isActive=True, isDelete=False)
        name = request.query_params.get('name', None)
        category_id = request.query_params.get('categoryId', None)
        brand_id = request.query_params.get('brandId', None)
        is_used = request.query_params.get('isUsed', None)

        if name:
            products = products.filter(name__icontains=name)
        if category_id:
            products = products.filter(categoryId=category_id)
        if brand_id:
            products = products.filter(brandId=brand_id)
        if is_used:
            products = products.filter(is_used=is_used)

        # Apply pagination
        paginator = self.pagination_class()
        paginated_products = paginator.paginate_queryset(products, request, view=self)
        serializer = None
        if request.user.id is not None:
            serializer = ProductViewWithUserSerializer(paginated_products, many=True,
                                                       context={'userId': request.user.id})
        else:
            serializer = ProductViewSerializer(paginated_products, many=True, )

        return local_response('create', True, "ok", '', paginator.get_paginated_response(serializer.data).data)


class ProductDetailAPIView(APIView):
    serializer_class = ProductViewSerializer

    def get(self, request, id_or_slug):
        try:
            if id_or_slug.isdigit():
                product = Product.objects.select_related('brandId').prefetch_related('categoryId').get(
                    Q(id=id_or_slug),
                    isActive=True,
                    isDelete=False
                )
            else:
                product = Product.objects.select_related('brandId').prefetch_related('categoryId').get(
                    Q(slug=id_or_slug),
                    isActive=True,
                    isDelete=False
                )
            serializer = ProductViewSerializer(product)
            return local_response('create', True, "ok", '', serializer.data)
        except Product.DoesNotExist:
            # Handle the case where the product does not exist
            return local_response('notFound', True, "Product not found", '', None)


class ProductCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProductCreateSerializer

    def post(self, request):

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return local_response('create', True, "ok", '', serializer.data)
        else:
            return validation_response(serializer.errors)


class ProductUpdateManyAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProductUpdateSerializer

    def patch(self, request):
        # print(request.data['brandId'])
        # itemIds = request.query_params.get('productIds', None)
        # if itemIds is None:
        #     return local_response('badReq', False, "وارد کردن ایدی محصولات اجباری است", 'productIds', None)
        # if request.data['productIds'] is None:
        #     return local_response('badReq', False, "وارد کردن ایدی محصولات اجباری است", 'productIds', None)
        # itemIds = request.data['productIds']
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return validation_response(serializer.errors)
        values = serializer.data
        values.pop('productIds')
        print(values)
        instances = Product.objects.filter(pk=2)
        newSerializer = ProductSerializer(instances, data=request.data, partial=True)
        newSerializer.is_valid(raise_exception=True)

        # if not newSerializer.is_valid():
        #     return validation_response(newSerializer.errors)
        newSerializer.save()

        # print(values)
        # Product.objects.filter(id__in=request.data['productIds']).update(isUsed=False)
        return local_response('create', True, "ok", '', None)

        # # instance = YourModel.objects.get(pk=pk)
        # serializer = self.serializer_class(data=request.data)
        # if serializer.is_valid():
        #     serializer.save()
        #     return local_response('create', True, "ok", '', serializer.data)
        # else:
        #     return validation_response(serializer.errors)
# class ProductUpdateAPIView(APIView):
#     serializer_class = ProductUpdateSerializer
#
#     def put(self, request, id_or_slug):
#         try:
#             if id_or_slug.isdigit():
#                 product = Product.objects.select_related('brandId').prefetch_related('categoryId').get(
#                     Q(id=id_or_slug),
#                     is_active=True,
#                     is_delete=False
#                 )
#             else:
#                 product = Product.objects.select_related('brandId').prefetch_related('categoryId').get(
#                     Q(slug=id_or_slug),
#                     is_active=True,
#                     is_delete=False
#                 )
#             serializer = self.serializer_class(product, data=request.data, partial=True)
#             serializer.is_valid(raise_exception=True)
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         except Product.DoesNotExist:
#             # Handle the case where the product does not exist
#             return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)


# class ProductDestroyAPIView(APIView):
#     serializer_class = ProductSerializer
#
#     def delete(self, request, id_or_slug: str):
#         try:
#             if id_or_slug.isdigit():
#                 product = Product.objects.select_related('brandId').prefetch_related('categoryId').get(
#                     Q(id=id_or_slug),
#                     isActive=True,
#                     isDelete=False
#                 )
#             else:
#                 product = Product.objects.select_related('brandId',).prefetch_related('categoryId').get(
#                     Q(slug=id_or_slug),
#                     isActive=True,
#                     isDelete=False
#                 )
#             product.isActive = False
#             product.isDelete = True
#             product.save()
#             serializer = self.serializer_class(product)
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         except Product.DoesNotExist:
#             # Handle the case where the product does not exist
#             return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)


# class ProductSearchAPIView(APIView):
#     serializer_class = ProductSerializer
#
#     def get(self, request):
#         query = request.query_params.get('q', None)
#         print('111111111111111111111111111111111111')
#         try:
#             products = Product.objects.select_related('brandId').prefetch_related('categoryId').filter(
#                 Q(description__icontains=query) | Q(name__icontains=query),
#                 isActive=True, isDelete=False
#             ).order_by('id')
#             print('222222222222222222222222222222222222222')
#
#         except Product.DoesNotExist:
#             print('333333333333333333333333333333333333333333333333')
#             return Response({"message": "No products found."}, status=status.HTTP_404_NOT_FOUND)
#         print('44444444444444444444444444444444444444444444444444')
#
#         if products:
#             print('5555555555555555555555555555555555555555555555555')
#             serializer = self.serializer_class(products, many=True)
#             print(serializer.data)
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response({"message": "No products found."}, status=status.HTTP_404_NOT_FOUND)
