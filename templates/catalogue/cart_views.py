from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from .models import Product
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id, is_available=True)
    cart = request.session.get("cart", {})
    pid_str = str(product_id)
    cart[pid_str] = cart.get(pid_str, 0) + 1
    request.session["cart"] = cart
    messages.success(request, f"Added {product.name} to your cart.")
    return redirect("catalogue:shop_detail", slug=product.shop.slug)