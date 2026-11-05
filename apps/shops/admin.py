from django.contrib import admin
from .models import ShopProfile
 
@admin.register(ShopProfile)
class ShopProfileAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "is_approved", "is_open", "created_at")
    list_filter = ("is_approved", "is_open")
    search_fields = ("name", "owner__email", "phone")
    prepopulated_fields = {"slug": ("name",)}
