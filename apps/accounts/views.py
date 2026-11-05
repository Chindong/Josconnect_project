from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import SignUpForm
from .models import User
 
def signup(request, role):
    allowed = {
        "customer": User.Role.CUSTOMER,
        "shop": User.Role.SHOP_OWNER,
        "rider": User.Role.RIDER,
    }
    selected_role = allowed.get(role)
    if not selected_role:
        return redirect("catalogue:home")
 
    form = SignUpForm(request.POST or None, role=selected_role)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        if selected_role == User.Role.CUSTOMER:
            login(request, user)
            return redirect("catalogue:home")
        messages.success(request, "Registration received. Your account awaits approval.")
        return redirect("accounts:login")
    return render(request, "accounts/signup.html", {"form": form, "role": role})
