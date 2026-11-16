from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages
from apps.accounts.forms import SignUpForm
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from apps.accounts.models import User
from .models import RiderProfile
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.http import HttpResponseForbidden, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
from apps.accounts.models import User
from apps.orders.models import Order
from .models import RiderProfile, Delivery
from .services import assign_order_to_rider

@transaction.atomic
def rider_signup(request):
    user_form = SignUpForm(request.POST or None, role=User.Role.RIDER)
    profile_form = RiderProfileForm(request.POST or None)

    if request.method == "POST" and user_form.is_valid() and profile_form.is_valid():
        user = user_form.save()
        rider_profile = profile_form.save(commit=False)
        rider_profile.user = user
        rider_profile.is_approved = False
        rider_profile.is_available = False
        rider_profile.save()
        
        messages.success(
        request,
        "Rider registration submitted. An administrator will verify your details before activation.")

        return redirect("accounts:login")

    return render(request, "dispatch/signup.html", {
        "user_form": user_form,
        "profile_form": profile_form})

@login_required
@require_POST
def toggle_availability(request):
    if request.user.role != User.Role.RIDER:
        return HttpResponseForbidden("Rider account required.")
    rider = RiderProfile.objects.get(user=request.user, is_approved=True)
    rider.is_available = not rider.is_available
    rider.save(update_fields=["is_available"])
    return render(request, "partials/rider_availability.html", {"rider": rider})

@login_required
def rider_dashboard(request):
    if request.user.role != User.Role.RIDER:
        return HttpResponseForbidden("Rider access required.")
    rider = get_object_or_404(RiderProfile, user=request.user)
    active_deliveries = rider.deliveries.exclude(
        status__in=[Delivery.Status.DELIVERED, Delivery.Status.FAILED]
    ).select_related("order", "order__shop")
    ready_orders = Order.objects.filter(
        status=Order.Status.READY,
        delivery__isnull=True
    ).select_related("shop") if (rider.is_approved and rider.is_available) else []
    return render(request, "dispatch/dashboard.html", {
        "rider": rider,
        "active_deliveries": active_deliveries,
        "ready_orders": ready_orders,
    })
@login_required
@require_POST
def toggle_availability(request):
    if request.user.role != User.Role.RIDER:
        return HttpResponseForbidden("Rider access required.")
    rider = get_object_or_404(RiderProfile, user=request.user, is_approved=True)
    rider.is_available = not rider.is_available
    rider.save(update_fields=["is_available"])
    return render(request, "partials/rider_availability.html", {"rider": rider})
@login_required
@require_POST
def assign_delivery_view(request, order_id):
    # Allow either an Admin assigning a chosen rider OR an approved Rider self claiming
    if request.user.role == User.Role.RIDER:
        rider = get_object_or_404(RiderProfile, user=request.user, 
is_approved=True)
        target_rider_id = rider.pk
    elif request.user.role == User.Role.ADMIN or request.user.is_staff:
        target_rider_id = request.POST.get("rider_id")
        if not target_rider_id:
            return HttpResponseBadRequest("A valid rider_id must be provided.")
    else:
        return HttpResponseForbidden("Not authorized to assign deliveries.")

    try:
        delivery = assign_order_to_rider(order_id=order_id, rider_id=int(target_rider_id))
    except (ValidationError, Order.DoesNotExist, RiderProfile.DoesNotExist) as exc:
        return HttpResponseBadRequest(str(exc))

    return render(request, "partials/delivery_assigned_badge.html", {"delivery": delivery})