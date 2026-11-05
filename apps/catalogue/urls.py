from django.urls import path
from . import views
 
app_name = "catalogue"
urlpatterns = [
    path("", views.home, name="home"),
    path("shop/<slug:slug>/", views.shop_detail, name="shop_detail"),
]
