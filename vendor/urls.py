from django.urls import path

from vendor.apis.CityView import CityCreateView, CityListView, CityDetailView, CityUpdateView, CityDeleteView
from vendor.apis.VendorView import VendorCreateAPIView, VendorListAPIView, VendorDetailAPIView
from vendor.apis.ClickHistoryView import ClickHistoryCreateView

urlpatterns = [

    # city
    path('cities/findAll/', CityListView.as_view(), name='city_list'),
    path('cities/detail/<int:id>/', CityDetailView.as_view(), name='city_detail'),
    path('cities/create/', CityCreateView.as_view(), name='city_create'),
    path('cities/update/<int:id>/', CityUpdateView.as_view(), name='city_update'),
    path('cities/delete/<int:id>/', CityDeleteView.as_view(), name='city_delete'),

    # vendor
    path('vendors/create/', VendorCreateAPIView.as_view(), name='vendor_create'),
    path('vendors/findAll/', VendorListAPIView.as_view(), name='vendor_list'),
    path('vendors/detail/<str:id_or_slug>/', VendorDetailAPIView.as_view(), name='vendor_detail'),

    # clickHistory
    path('clickHistory/create/', ClickHistoryCreateView.as_view(), name='click_history_create'),
]
