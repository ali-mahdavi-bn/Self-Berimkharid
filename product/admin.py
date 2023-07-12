from django.contrib import admin

from .models import Product, Category, Brand, ProductItem, Like


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    search_fields = ('title',)
    ordering = ('title',)


class BrandAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'slug', 'isActive', 'isDelete', 'createdAt', 'updatedAt')
    list_filter = ('isActive', 'isDelete')
    search_fields = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}


class ProductAdmin(admin.ModelAdmin):
    autocomplete_fields = ('categoryId', 'brandId', 'pictureGallery')
    list_display = (
        'id', 'name', 'isUsed', 'isActive', 'isDelete', 'createdAt',
        'updatedAt')
    list_filter = ('isUsed', 'isActive', 'isDelete', 'createdAt', 'updatedAt')
    search_fields = ('name',)
    # list_select_related = ('brandId', 'pictureGallery')
    readonly_fields = ('createdAt', 'updatedAt')


class ProductItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'price', 'link', 'inStock', 'recordedAt', 'productId')
    list_filter = ('inStock', 'recordedAt')
    search_fields = ('price', 'link')
    date_hierarchy = 'recordedAt'
    ordering = ('-recordedAt',)


class LikeItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'productId', 'userId')
    list_filter = ('createdAt',)
    search_fields = ('productId', 'userId')
    date_hierarchy = 'createdAt'
    ordering = ('-createdAt',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductItem, ProductItemAdmin)
admin.site.register(Like, LikeItemAdmin)
