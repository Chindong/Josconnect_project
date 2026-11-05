from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
 
class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "phone_number")
 
    def __init__(self, *args, role=User.Role.CUSTOMER, **kwargs):
        super().__init__(*args, **kwargs)
        self.role = role
        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control"})
 
    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = self.role
        if commit:
            user.save()
        return user
