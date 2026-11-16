from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import SignUpForm
from .models import User
from apps.dispatch.forms import RiderProfileForm

def signup_choice(request):
    """Displays the 3-way role selector before registration."""
    return render(request, "accounts/signup_choice.html")


def signup(request, role):
    allowed = {
        "customer": User.Role.CUSTOMER,
        "shop": User.Role.SHOP_OWNER,
        "rider": User.Role.RIDER,
    }
    selected_role = allowed.get(role)
    if not selected_role:
        return redirect("accounts:signup_choice")

    form = SignUpForm(request.POST or None, role=selected_role)
    rider_form = RiderProfileForm(request.POST or None) if selected_role == User.Role.RIDER else None

    if request.method == "POST":
        is_valid = form.is_valid() and (rider_form.is_valid() if rider_form else True)
        if is_valid:
            user = form.save()

            if selected_role == User.Role.RIDER and rider_form:
                rider_profile = rider_form.save(commit=False)
                rider_profile.user = user
                rider_profile.save()

            if selected_role == User.Role.CUSTOMER:
                login(request, user)
                return redirect("catalogue:home")

            messages.success(request, "Registration received. Your account awaits admin approval.")
            return redirect("accounts:login")

    return render(request, "accounts/signup.html", {
        "form": form,
        "rider_form": rider_form,
        "role": role,
    })


def custom_login(request):
    """Handles login with role selection and role-based dashboard redirection."""
    form = AuthenticationForm(request, data=request.POST or None)
    selected_role = request.POST.get("selected_role", "CUSTOMER")

    if request.method == "POST" and form.is_valid():
        user = form.get_user()

        # Verify the user's account matches the portal role they selected
        if user.role != selected_role and not user.is_superuser:
            messages.error(
                request,
                f"This account is registered as a {user.get_role_display()}, not a {dict(User.Role.choices).get(selected_role)}."
            )
            return render(request, "accounts/login.html", {"form": form, "selected_role": selected_role})

        login(request, user)

        # Redirect each role to their appropriate workspace
        if user.role == User.Role.RIDER:
            return redirect("dispatch:dashboard")
        elif user.role == User.Role.SHOP_OWNER:
            return redirect("shops:dashboard")  # Or your shop dashboard URL name
        return redirect("catalogue:home")

    return render(request, "accounts/login.html", {
        "form": form,
        "selected_role": selected_role
    })

