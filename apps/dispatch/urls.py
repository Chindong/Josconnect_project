from django.urls import path
from . import views
app_name = "dispatch"
urlpatterns = [
    path("signup/", views.rider_signup, name="signup"),
    path("dashboard/", views.rider_dashboard, name="dashboard"),
    path("availability/toggle/", views.toggle_availability, name="toggle_availability"),
    path("assign/<int:order_id>/", views.assign_delivery_view, name="assign_delivery"),
]
