# Register your models here.
from django.contrib import admin

from .models import Vendor
from .models import City


class VendorAdmin(admin.ModelAdmin):
    autocomplete_fields = ('pictureGallery',)

    list_display = ('id','name', 'nameEn', 'metaName', 'description', 'createdAt', 'updatedAt')
    list_filter = ('name', 'nameEn')
    search_fields = ('name', 'nameEn')
    ordering = ('-updatedAt',)


class CityAdmin(admin.ModelAdmin):
    list_display = ('title', 'createdAt', 'updatedAt')
    list_filter = ('title', )
    search_fields = ('title',)
    ordering = ('-updatedAt',)


admin.site.register(Vendor, VendorAdmin)
admin.site.register(City, CityAdmin)
