from django.urls import path
from . import views
app_name = "dispatch"
urlpatterns = [
    path("availability/toggle/", views.toggle_availability, name="toggle_availability"),
]
