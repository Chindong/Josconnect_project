from decimal import Decimal
from django.conf import settings
from django.db import models
from apps.shops.models import ShopProfile
 
class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Awaiting shop"
        ACCEPTED = "ACCEPTED", "Accepted"
        PREPARING = "PREPARING", "Preparing"
        READY = "READY", "Ready for pickup"
        DISPATCHED = "DISPATCHED", "Out for delivery"
        COMPLETED = "COMPLETED", "Completed"
        CANCELLED = "CANCELLED", "Cancelled"
 
    class PaymentMethod(models.TextChoices):
        COD = "COD", "Cash on delivery"
        TRANSFER = "TRANSFER", "Bank transfer"
        ONLINE = "ONLINE", "Online payment"
 
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT,
                                 related_name="orders")
    shop = models.ForeignKey(ShopProfile, on_delete=models.PROTECT, related_name="orders")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    payment_method = models.CharField(max_length=20, choices=PaymentMethod.choices)
    delivery_address = models.TextField()
    customer_phone = models.CharField(max_length=20)
    item_subtotal = models.DecimalField(max_digits=12, decimal_places=2)
    delivery_fee = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    platform_commission = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("100.00"))
    gateway_fee = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    customer_total = models.DecimalField(max_digits=12, decimal_places=2)
    is_paid = models.BooleanField(default=False)
    payment_reference = models.CharField(max_length=100, unique=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
 
    def __str__(self):
        return f"Order #{self.pk} - {self.status}"
 
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product_name = models.CharField(max_length=180)  # snapshot at order time
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    line_total = models.DecimalField(max_digits=12, decimal_places=2)
 
    def __str__(self):
        return f"{self.quantity} x {self.product_name}"
