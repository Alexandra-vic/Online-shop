from django.contrib import admin

from products.models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'description',
        'status',
    )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass