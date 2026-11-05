from decimal import Decimal
from django.db import transaction
from .models import Order, OrderItem
from apps.catalogue.models import Product
 
COMMISSION = Decimal("100.00")
 
@transaction.atomic
def create_order(*, customer, shop, cart_items, address, phone, payment_method, delivery_fee):
    subtotal = Decimal("0.00")
    validated = []
    for item in cart_items:
        product = Product.objects.select_for_update().get(
            pk=item["product_id"], shop=shop, is_available=True
        )
        qty = int(item["quantity"])
        if qty < 1 or (product.stock_quantity and qty > product.stock_quantity):
            raise ValueError("Requested quantity is unavailable.")
        line_total = product.price * qty
        subtotal += line_total
        validated.append((product, qty, line_total))
 
    commission = COMMISSION
    total = subtotal + delivery_fee + commission
    order = Order.objects.create(
        customer=customer, shop=shop, delivery_address=address, customer_phone=phone,
        payment_method=payment_method, item_subtotal=subtotal, delivery_fee=delivery_fee,
        platform_commission=commission, customer_total=total
    )
    for product, qty, line_total in validated:
        OrderItem.objects.create(order=order, product_name=product.name,
            unit_price=product.price, quantity=qty, line_total=line_total)
    return order
