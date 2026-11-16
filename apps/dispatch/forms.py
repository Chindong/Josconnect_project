from django import forms
from .models import RiderProfile


class RiderProfileForm(forms.ModelForm):
    class Meta:
        model = RiderProfile
        fields = ("vehicle_type", "plate_number")
        widgets = {
            "vehicle_type": forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "e.g., Motorcycle or Bicycle"}),
            "plate_number": forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "e.g., PLT-482QA"
}),
}
