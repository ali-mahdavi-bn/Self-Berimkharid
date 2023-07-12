from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView

from helper.response import local_response, validation_response
from product.models import Category
from product.serializers.CategorySerializer import CategoryViewSerializer, CategoryCreateSerializer, \
    TreeCategorySerializer


class CategoryListView(APIView):
    serializer_class = CategoryViewSerializer
    pagination_class = PageNumberPagination
    pagination_class.page_size_query_param = 'page_size'

    def get(self, request):
        queryset = self.get_queryset().order_by(request.query_params.get('order_by', 'id'))
        page_size = request.query_params.get('page_size', 20)
        if page_size:
            self.pagination_class.page_size = int(page_size)
        paginator = self.pagination_class()
        paginated_queryset = paginator.paginate_queryset(queryset, request, view=self)
        serializer = self.serializer_class(paginated_queryset, many=True)
        return local_response('found', True, "ok", '', paginator.get_paginated_response(serializer.data).data)

    def get_queryset(self):
        return Category.objects.filter(isActive=True, isDelete=False, parentId=None)


class CategoryDetailView(APIView):
    serializer_class = TreeCategorySerializer

    def get(self, request, id):
        try:
            my_model = Category.objects.get(pk=id)
        except Category.DoesNotExist:
            return local_response('notFound', True, "notFound", '', '')
        serializer = self.serializer_class(my_model)
        return local_response('found', True, "ok", '', serializer.data)


class CategoryCreateView(APIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = CategoryCreateSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # result = UploadShowSerializer(serializer.save())
            return local_response('create', True, "ok", '', serializer.data)
        else:
            return validation_response(serializer.errors)

# class BrandUpdateView(UpdateAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = BrandSerializer
#     lookup_field = 'id'
#     queryset = Brand.objects.all()


# class BrandDeleteView(APIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = BrandDeleteSerializer
#
#     def delete(self, request, id):
#         serializer = self.serializer_class(data={'id': id})
#         serializer.is_valid(raise_exception=True)
#
#         brand = serializer.validated_data['id']
#         brand.isDelete = True
#         brand.save()
#
#         return Response({'message': 'Brand deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
