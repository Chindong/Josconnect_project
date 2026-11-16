from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
 
app_name = "accounts"
urlpatterns = [
    # Role selection hub for registration
    path("signup/", views.signup_choice, name="signup_choice"),
    
    # Role-specific registration routes
    path("signup/<str:role>/", views.signup, name="signup"),
    
    # Login & Logout
    path("login/", views.custom_login, name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
]
