from __future__ import unicode_literals
from django.contrib import admin

from .models import ProductCategory


class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = (
        '__str__', 'product', 'product_place'
    )
    search_fields = (
        'product',
    )


admin.site.register(ProductCategory, ProductCategoryAdmin)