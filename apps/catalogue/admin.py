from django.contrib import admin
from .models import Category, Product
 
admin.site.register(Category)
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "shop", "price", "is_available", "stock_quantity")
    list_filter = ("is_available", "shop")
    search_fields = ("name", "shop__name")
