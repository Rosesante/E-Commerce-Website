from django.contrib import admin
from .models import Category, Product, ProductImage


# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "stock_quantity", "is_available", "created_at",)
    list_filter = ("category", "is_available", "created_at",)
    search_fields = ("name", "sku", "brand",)
    prepopulated_fields = { "slug": ("name",) }

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ( "product", "is_primary", "created_at", )
    list_filter = ("is_primary",)
    search_fields = ("product__name",)