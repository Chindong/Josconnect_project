from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseForbidden
from apps.orders.models import Order
@login_required
def update_order_status(request, order_id):
    if request.user.role != "SHOP_OWNER":
        return HttpResponseForbidden()
    order = get_object_or_404(Order, pk=order_id, 
shop=request.user.shop_profile)
    new_status = request.POST.get("status")
    if new_status in Order.Status.values:
        order.status = new_status
        order.save()
    return render(request, "partials/order_status_badge.html", {"order":order})