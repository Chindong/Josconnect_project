from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from apps.shops.models import ShopProfile
from .models import Product
 
def home(request):
    shops = ShopProfile.objects.filter(is_approved=True, is_open=True).order_by("name")
    query = request.GET.get("q", "").strip()
    products = Product.objects.filter(shop__is_approved=True, is_available=True)
    if query:
        products = products.filter(Q(name__icontains=query) | Q(shop__name__icontains=query))
    return render(request, "public/home.html", {"shops": shops, "products": products[:24], "query": query})
 
def shop_detail(request, slug):
    shop = get_object_or_404(ShopProfile, slug=slug, is_approved=True)
    products = shop.products.filter(is_available=True)
    return render(request, "shops/public_detail.html", {"shop": shop, "products": products})
