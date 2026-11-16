from django.contrib import admin
from .models import RiderProfile, Delivery

@admin.register(RiderProfile)
class RiderProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "vehicle_type", "plate_number", "is_approved", "is_available")
    list_filter = ("is_approved", "is_available", "vehicle_type")
    search_fields = ("user__email", "user__phone_number", "plate_number")

@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = ("order", "rider", "status", "assigned_at", "completed_at")
    list_filter = ("status",)
    search_fields = ("order__pk", "rider__user__email")