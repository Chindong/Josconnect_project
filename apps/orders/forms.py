from django import forms
from .models import Order
 
class CheckoutForm(forms.Form):
    address = forms.CharField(widget=forms.Textarea(attrs={"rows": 3}))
    phone = forms.CharField(max_length=20)
    payment_method = forms.ChoiceField(choices=Order.PaymentMethod.choices)
