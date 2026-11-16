from django.db import transaction
from django.core.exceptions import ValidationError
from apps.orders.models import Order
from .models import RiderProfile, Delivery


@transaction.atomic
def assign_order_to_rider(*, order_id: int, rider_id: int) -> Delivery:
    # Lock the order row to block concurrent claims
    order = Order.objects.select_for_update().get(pk=order_id)

    if order.status != Order.Status.READY:
        raise ValidationError("Order must be marked READY before rider assignment.")
    
    if hasattr(order, "delivery"):
        raise ValidationError("This order has already been assigned to a dispatch rider.")
    
    # Lock the rider row and confirm approval + availability
    rider = RiderProfile.objects.select_for_update().get(pk=rider_id)

    if not rider.is_approved:
        raise ValidationError("Unapproved riders cannot receive dispatch assignments.")

    if not rider.is_available:
        raise ValidationError("Selected rider is currently offline or unavailable.")

    # Create delivery record and update order status atomically
    delivery = Delivery.objects.create(
        order=order,
        rider=rider,
        status=Delivery.Status.ASSIGNED
    )

    order.status = Order.Status.DISPATCHED
    order.save(update_fields=["status"])
    
    return delivery