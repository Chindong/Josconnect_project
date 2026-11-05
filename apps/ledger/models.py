from django.db import models
from apps.orders.models import Order
 
class LedgerEntry(models.Model):
    class EntryType(models.TextChoices):
        COMMISSION = "COMMISSION", "JosConnect commission"
        GATEWAY_FEE = "GATEWAY_FEE", "Payment processing fee"
        SHOP_DUE = "SHOP_DUE", "Shop amount due"
        RIDER_DUE = "RIDER_DUE", "Rider amount due"
        REFUND = "REFUND", "Refund"
 
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name="ledger_entries")
    entry_type = models.CharField(max_length=20, choices=EntryType.choices)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    reference = models.CharField(max_length=120, blank=True)
    is_reconciled = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
 
    class Meta:
        ordering = ["created_at"]
