from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render
from django.views.decorators.http import require_POST
from apps.accounts.models import User
from .models import RiderProfile
 
@login_required
@require_POST
def toggle_availability(request):
    if request.user.role != User.Role.RIDER:
        return HttpResponseForbidden("Rider account required.")
    rider = RiderProfile.objects.get(user=request.user, is_approved=True)
    rider.is_available = not rider.is_available
    rider.save(update_fields=["is_available"])
    return render(request, "partials/rider_availability.html", {"rider": rider})
