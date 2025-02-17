from django import forms
from .models import BusinessProfile, Product, Service

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
BOOLEAN_CHOICES = [(True, "Sí"), (False, "No")]
class CompleteBusinessProfileForm(forms.ModelForm):
    

    class Meta:
        model = BusinessProfile
        fields = [
            "company_name",
            "show_company_name",
            "company_logo",
            "show_company_logo",
            "assistant_image",
            "show_assistant_image",
            "background_image",
            "background_color",
            "form_background_color",
            "button_background_color",
            "button_text_color",
            "chat_text_color",
            "company_name",
            "assistant_url_name",
            "description",
            "contact_email",
            "phone",
            "website",
            "address",
            "business_hours",
            "social_media"
        ]
        widgets = {
            "company_name": forms.TextInput(attrs={"class": "form-control", "placeholder": ""}),
            "show_company_name": forms.Select(choices=BOOLEAN_CHOICES, attrs={"class": "form-control"}),
            "company_logo": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "show_company_logo": forms.Select(choices=BOOLEAN_CHOICES, attrs={"class": "form-control"}),
            "assistant_image": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "show_assistant_image": forms.Select(choices=BOOLEAN_CHOICES, attrs={"class": "form-control"}),
            "background_image":forms.ClearableFileInput(attrs={"class": "form-control"}),
            "background_color":forms.TextInput(attrs={"class": "form-control", "placeholder": ""}),
            "form_background_color":forms.TextInput(attrs={"class": "form-control", "placeholder": ""}),
            "button_background_color":forms.TextInput(attrs={"class": "form-control", "placeholder": ""}),
            "button_text_color":forms.TextInput(attrs={"class": "form-control", "placeholder": ""}),
            "chat_text_color":forms.TextInput(attrs={"class": "form-control", "placeholder": ""}),
            "company_name":forms.TextInput(attrs={"class": "form-control", "placeholder": ""}),
            "assistant_url_name":forms.TextInput(attrs={"class": "form-control", "placeholder": "Nombre para el asiste. Por ejemplo: zapatosmadrid" }),
            "description":forms.Textarea(attrs={"class": "form-control", "rows": 15, "placeholder": ""}),
            "contact_email":forms.TextInput(attrs={"class": "form-control", "placeholder": ""}),
            "phone":forms.TextInput(attrs={"class": "form-control", "placeholder": ""}),
            "website":forms.TextInput(attrs={"class": "form-control", "placeholder": ""}),
            "address":forms.TextInput(attrs={"class": "form-control", "placeholder": ""}),
            "business_hours":forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Ejemplo: Lunes a viernes de 8:00 a 13:30 y de 16:30 a 19:00. Sábados de 9:00 a 14:00."}),
            "social_media":forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "","value":"{'facebook': 'url', 'instagram': 'url'}"}),
        }


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "description", "price", "available", "image"]
        
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Nombre del producto"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Descripción del producto"}),
            "price": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Precio"}),
            "available": forms.Select(choices=[(True, "Disponible"), (False, "No Disponible")], attrs={"class": "form-control"}),
            "image": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }



class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ["name", "description", "price", "available", "image"]
        
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Nombre del servicio"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Descripción del servicio"}),
            "price": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Precio"}),
            "available": forms.Select(choices=[(True, "Disponible"), (False, "No Disponible")], attrs={"class": "form-control"}),
            "image": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }