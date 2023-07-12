from django.urls import path

from upload.apis.UploadView import UploadCreateView

urlpatterns = [

    path('upload/create/', UploadCreateView.as_view(), name='upload_create'),


]
