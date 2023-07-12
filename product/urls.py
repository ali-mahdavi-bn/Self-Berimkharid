from django.urls import path

from product.apis.BrandsView import BrandListView, BrandDeleteView, BrandCreateView, BrandDetailView, BrandUpdateView
from product.apis.CategoryView import CategoryCreateView, CategoryListView ,CategoryDetailView
from product.apis.ProductView import  ProductCreateAPIView ,ProductListAPIView,ProductDetailAPIView,ProductUpdateManyAPIView
from product.apis.LikeView import LikeCreateView

urlpatterns = [

    # product
    path('products/findAll/', ProductListAPIView.as_view(), name='product_list'),
    path('products/detail/<str:id_or_slug>/', ProductDetailAPIView.as_view(), name='product_retrieve'),
    path('products/create/', ProductCreateAPIView.as_view(), name='product_create'),
    # path('products/updateMany/', ProductUpdateManyAPIView.as_view(), name='product_update_many'),

    # path('product/update/<str:id_or_slug>/', ProductUpdateAPIView.as_view(), name='product_update'),
    # path('product/delete/<str:id_or_slug>/', ProductDestroyAPIView.as_view(), name='product_destroy'),
    # path('product/search/', ProductSearchAPIView.as_view(), name='product_search'),

    # like
    path('likes/create/', LikeCreateView.as_view(), name='like_create'),
    # brand
    path('brands/findAll/', BrandListView.as_view(), name='brand_list'),
    path('brands/detail/<int:id>/', BrandDetailView.as_view(), name='brand_detail'),
    path('brands/create/', BrandCreateView.as_view(), name='brand_create'),
    path('brands/update/<int:id>/', BrandUpdateView.as_view(), name='brand_update'),
    path('brands/delete/<int:id>/', BrandDeleteView.as_view(), name='brand_delete'),

    # category
    path('categories/create/', CategoryCreateView.as_view(), name='category_create'),
    path('categories/findAll/', CategoryListView.as_view(), name='category_list'),
    path('categories/detail/<int:id>/', CategoryDetailView.as_view(), name='category_detail'),

]
