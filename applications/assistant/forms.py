from django import forms
from .models import BusinessProfile, Product, Service, FAQ

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
from django import forms
from .models import BusinessProfile

# Definición de opciones booleanas
BOOLEAN_CHOICES = [(True, "Sí"), (False, "No")]

class CompleteBusinessProfileForm(forms.ModelForm):
    class Meta:
        model = BusinessProfile
        fields = [
            # Información de la empresa
            "company_name",
            "show_company_name",
            "company_logo",
            "show_company_logo",
            "assistant_url_name",
            "description",
            "contact_email",
            "phone",
            "show_phone_call",
            "website",
            "address",
            "business_hours",
            "social_media",
            "facebook",
            "show_facebook_button",
            "whatsapp",
            "show_whatsapp_button",
            "instagram",
            "show_instagram_button",
            "youtube",
            "show_youtube_button",
            "tiktok",
            "show_tiktok_button",
            "twitterx",
            "show_twitterx_button",
            "telegram",
            "show_telegram_button",

            # Imágenes y visualización
            "assistant_image",
            "show_assistant_image",
            "background_image",
            "show_background_image",
            "show_return_to_web",

            # Colores personalizados
            "background_color",
            "show_background_color",
            "form_background_color",
            "button_background_color",
            "button_text_color",
            "chat_customer_text_color",
            "chat_assistant_text_color",
        ]
        
        widgets = {
            # Campos de texto
            "company_name": forms.TextInput(attrs={"class": "form-control"}),
            "assistant_url_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Nombre para el asiste. Por ejemplo: zapatosmadrid"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 15}),
            "contact_email": forms.TextInput(attrs={"class": "form-control"}),
            "phone": forms.TextInput(attrs={"class": "form-control"}),
            "website": forms.TextInput(attrs={"class": "form-control"}),
            "address": forms.TextInput(attrs={"class": "form-control"}),
            "business_hours": forms.Textarea(attrs={
                "class": "form-control", 
                "rows": 3, 
                "placeholder": "Ejemplo: Lunes a viernes de 8:00 a 13:30 y de 16:30 a 19:00. Sábados de 9:00 a 14:00."
            }),
            "social_media": forms.Textarea(attrs={
                "class": "form-control", 
                "rows": 3, 
                "placeholder": "{'facebook':'https://www.facebook.com/tuempresa'}"
            }),
            "facebook": forms.TextInput(attrs={"class": "form-control"}),
            "whatsapp": forms.TextInput(attrs={"class": "form-control"}),
            "instagram": forms.TextInput(attrs={"class": "form-control"}),
            "youtube": forms.TextInput(attrs={"class": "form-control"}),
            "tiktok": forms.TextInput(attrs={"class": "form-control"}),
            "twitterx": forms.TextInput(attrs={"class": "form-control"}),
            "telegram": forms.TextInput(attrs={"class": "form-control"}),

            # Campos booleanos (Sí/No)
            "show_company_name": forms.Select(choices=BOOLEAN_CHOICES, attrs={"class": "form-control"}),
            "show_company_logo": forms.Select(choices=BOOLEAN_CHOICES, attrs={"class": "form-control"}),
            "show_assistant_image": forms.Select(choices=BOOLEAN_CHOICES, attrs={"class": "form-control"}),
            "show_background_image": forms.Select(choices=BOOLEAN_CHOICES, attrs={"class": "form-control"}),
            "show_background_color": forms.Select(choices=BOOLEAN_CHOICES, attrs={"class": "form-control"}),
            "show_phone_call": forms.Select(choices=BOOLEAN_CHOICES, attrs={"class": "form-control"}),
            "show_return_to_web": forms.Select(choices=BOOLEAN_CHOICES, attrs={"class": "form-control"}),
            
            "show_facebook_button": forms.Select(choices=BOOLEAN_CHOICES, attrs={"class": "form-control"}),
            "show_whatsapp_button": forms.Select(choices=BOOLEAN_CHOICES, attrs={"class": "form-control"}),
            "show_instagram_button": forms.Select(choices=BOOLEAN_CHOICES, attrs={"class": "form-control"}),
            "show_youtube_button": forms.Select(choices=BOOLEAN_CHOICES, attrs={"class": "form-control"}),
            "show_tiktok_button": forms.Select(choices=BOOLEAN_CHOICES, attrs={"class": "form-control"}),
            "show_twitterx_button": forms.Select(choices=BOOLEAN_CHOICES, attrs={"class": "form-control"}),
            "show_telegram_button": forms.Select(choices=BOOLEAN_CHOICES, attrs={"class": "form-control"}),

            # Campos de archivos
            "company_logo": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "assistant_image": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "background_image": forms.ClearableFileInput(attrs={"class": "form-control"}),

            # Campos de selección de color
            "background_color": forms.TextInput(attrs={"type": "color", "class": "form-control form-control-color w-100", "title": "Choose a color"}),
            "form_background_color": forms.TextInput(attrs={"type": "color", "class": "form-control form-control-color w-100", "title": "Choose a color"}),
            "button_background_color": forms.TextInput(attrs={"type": "color", "class": "form-control form-control-color w-100", "id": "myColor", "title": "Choose a color"}),
            "button_text_color": forms.TextInput(attrs={"type": "color", "class": "form-control form-control-color w-100", "title": "Choose a color"}),
            "chat_customer_text_color": forms.TextInput(attrs={"type": "color", "class": "form-control form-control-color w-100", "title": "Choose a color"}),
            "chat_assistant_text_color": forms.TextInput(attrs={"type": "color", "class": "form-control form-control-color w-100", "title": "Choose a color"}),
        }


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "description", "price", "available", "image","product_url","offer","offer_price","product_image1_url","product_image2_url","product_image3_url"]
        
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Nombre del producto"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Descripción del producto"}),
            "price": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Precio"}),
            "available": forms.Select(choices=[(True, "Disponible"), (False, "No Disponible")], attrs={"class": "form-control"}),
            "image": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "offer": forms.Select(choices=BOOLEAN_CHOICES, attrs={"class": "form-control"}),
            "product_url":forms.TextInput(attrs={"class": "form-control", "placeholder": ""}),
            "offer_price": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Precio oferta"}),
            "product_image1_url":forms.TextInput(attrs={"class": "form-control", "placeholder": ""}),
            "product_image2_url":forms.TextInput(attrs={"class": "form-control", "placeholder": ""}),
            "product_image3_url":forms.TextInput(attrs={"class": "form-control", "placeholder": ""}),
            
        }

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ["name", "description", "price", "available", "image","service_url","offer","offer_price","service_image1_url","service_image2_url","service_image3_url"]
        
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Nombre del servicio"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Descripción del servicio"}),
            "price": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Precio"}),
            "available": forms.Select(choices=[(True, "Disponible"), (False, "No Disponible")], attrs={"class": "form-control"}),
            "image": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "offer": forms.Select(choices=BOOLEAN_CHOICES, attrs={"class": "form-control"}),
            "service_url":forms.TextInput(attrs={"class": "form-control", "placeholder": ""}),
            "offer_price": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Precio oferta"}),
            "service_image1_url":forms.TextInput(attrs={"class": "form-control", "placeholder": ""}),
            "service_image2_url":forms.TextInput(attrs={"class": "form-control", "placeholder": ""}),
            "service_image3_url":forms.TextInput(attrs={"class": "form-control", "placeholder": ""}),
            
        }


class FAQForm(forms.ModelForm):
    class Meta:
        model = FAQ
        fields = ["question", "answer"]
        
        widgets = {
            "question": forms.TextInput(attrs={"class": "form-control", "placeholder": "Pregunta"}),
            "answer": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Respuesta"}),            
        }