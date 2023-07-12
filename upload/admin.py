from django.contrib import admin

from .models import Upload


class UploadAdmin(admin.ModelAdmin):
    list_display = ('bucketName', 'path', 'isActive', 'isDelete', 'createdAt', 'updatedAt')
    list_filter = ('isActive', 'isDelete')
    search_fields = ('bucketName', 'path')
    ordering = ('-updatedAt',)


admin.site.register(Upload, UploadAdmin)
