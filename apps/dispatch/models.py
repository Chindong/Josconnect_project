from django.conf import settings
from django.db import models
from apps.orders.models import Order
 
class RiderProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT,
                                related_name="rider_profile")
    vehicle_type = models.CharField(max_length=40)
    plate_number = models.CharField(max_length=20, blank=True)
    is_approved = models.BooleanField(default=False)
    is_available = models.BooleanField(default=False)
 
    def __str__(self):
        return self.user.get_full_name() or self.user.email
 
class Delivery(models.Model):
    class Status(models.TextChoices):
        ASSIGNED = "ASSIGNED", "Assigned"
        PICKED_UP = "PICKED_UP", "Picked up"
        ON_THE_WAY = "ON_THE_WAY", "On the way"
        DELIVERED = "DELIVERED", "Delivered"
        FAILED = "FAILED", "Failed"
 
    order = models.OneToOneField(Order, on_delete=models.PROTECT, related_name="delivery")
    rider = models.ForeignKey(RiderProfile, on_delete=models.PROTECT, related_name="deliveries")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ASSIGNED)
    assigned_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
