import json
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from apps.shops.models import ShopProfile
from .forms import CheckoutForm
from .services import create_order
 
@login_required
def checkout(request, shop_id):
    shop = get_object_or_404(ShopProfile, pk=shop_id, is_approved=True, is_open=True)
    # MVP cart is held in the session. Browser values are revalidated in services.py.
    cart = request.session.get("cart", {})
    items = [{"product_id": int(pid), "quantity": int(qty)} for pid, qty in cart.items()]
    form = CheckoutForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        try:
            order = create_order(
                customer=request.user, shop=shop, cart_items=items,
                address=form.cleaned_data["address"], phone=form.cleaned_data["phone"],
                payment_method=form.cleaned_data["payment_method"],
                delivery_fee=Decimal("500.00")
            )
        except (ValueError, KeyError):
            messages.error(request, "Your cart has changed. Please review it and try again.")
        else:
            request.session["cart"] = {}
            return redirect("orders:detail", pk=order.pk)
    return render(request, "orders/checkout.html", {"form": form, "shop": shop})
 
@login_required
def order_detail(request, pk):
    from .models import Order
    order = get_object_or_404(Order, pk=pk, customer=request.user)
    return render(request, "orders/detail.html", {"order": order})
