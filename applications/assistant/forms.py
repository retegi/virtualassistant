from django import forms
from .models import BusinessProfile

class BusinessProfileForm(forms.ModelForm):
    

    class Meta:
        model = BusinessProfile
        fields = [
            "company_name", "assistant_url_name", "description", "contact_email", "phone",
            "website", "address", "business_hours"
        ]
        widgets = {
            "company_name": forms.TextInput(attrs={"class": "form-control", "placeholder": ""}),
            "assistant_url_name": forms.TextInput(attrs={"class": "form-control", "placeholder": ""}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": ""}),
            "contact_email": forms.EmailInput(attrs={"class": "form-control", "placeholder": ""}),
            "phone": forms.TextInput(attrs={"class": "form-control", "placeholder": ""}),
            "website": forms.URLInput(attrs={"class": "form-control", "placeholder": ""}),
            "address": forms.Textarea(attrs={"class": "form-control", "rows": 2, "placeholder": ""}),
            "business_hours": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": ""}),
        }


