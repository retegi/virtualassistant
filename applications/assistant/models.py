from django.db import models
from django.contrib.auth.models import User

class BusinessProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="business_profile")
    company_name = models.CharField(max_length=255, verbose_name="Nombre de la Empresa")
    show_company_name = models.BooleanField(default=True, verbose_name="Mostrar nombre de la empresa", blank=True, null=True)
    company_logo = models.ImageField(upload_to='assistant/company-logo/', verbose_name="Logo de empresa", blank=True, null=True)
    show_company_logo = models.BooleanField(default=True, verbose_name="Mostrar logo empresa", blank=True, null=True)
    assistant_image = models.ImageField(upload_to='assistant/assistant-image/', verbose_name="Imagen del asistente", blank=True, null=True)
    show_assistant_image = models.BooleanField(default=True, verbose_name="Mostrar imagen del asistente", blank=True, null=True)
    background_image = models.ImageField(upload_to='assistant/background-image/', verbose_name="Imagen de fondo", blank=True, null=True)
    show_background_image = models.BooleanField(default=True, verbose_name="Mostrar imagen de fondo", blank=True, null=True)
    background_color = models.CharField(max_length=255, verbose_name="Color HTML de fondo de página", default="white", blank=True, null=True)
    show_background_color = models.BooleanField(default=True, verbose_name="Mostrar color de fondo", blank=True, null=True)
    form_background_color = models.CharField(max_length=255, verbose_name="Color HTML de fondo de formulario", default="#f8f9fa", blank=True, null=True)
    button_background_color = models.CharField(max_length=255, verbose_name="Color HTML de fondo del botón", default="#28a745", blank=True, null=True)
    button_text_color = models.CharField(max_length=255, verbose_name="Color HTML de texto del botón", default="white", blank=True, null=True)
    chat_customer_text_color = models.CharField(max_length=255, verbose_name="Color HTML del texto del chat del cliente", default="#333", blank=True, null=True)
    chat_assistant_text_color = models.CharField(max_length=255, verbose_name="Color HTML del texto del chat del asistente", default="#333", blank=True, null=True)
    assistant_url_name = models.CharField(max_length=255, blank=True, null=True, unique=True)
    description = models.TextField(verbose_name="Descripción de la Empresa. Indícale al asistente sobre la empresa y a qué se dedica.", blank=True, null=True)
    contact_email = models.EmailField(verbose_name="Correo Electrónico de Contacto", blank=True, null=True)
    phone = models.CharField(max_length=20, verbose_name="Teléfono", blank=True, null=True)
    show_phone_call = models.BooleanField(default=True, verbose_name="Mostrar botón llamar", blank=True, null=True)
    show_return_to_web = models.BooleanField(default=True, verbose_name="Mostrar botón ir a web", blank=True, null=True)
    website = models.URLField(verbose_name="Sitio Web", blank=True, null=True)
    address = models.TextField(verbose_name="Dirección", blank=True, null=True)

    business_hours = models.TextField(verbose_name="Horario de Atención", blank=True, null=True)  # Guardado como JSON
    
    facebook = models.URLField(verbose_name="Url completa de facebook", blank=True, null=True)
    show_facebook_button = models.BooleanField(default=True, verbose_name="Mostrar botón facebook", blank=True, null=True)
    whatsapp = models.URLField(verbose_name="Url completa de whatsapp", blank=True, null=True)
    show_whatsapp_button = models.BooleanField(default=True, verbose_name="Mostrar botón whatsapp", blank=True, null=True)
    instagram = models.URLField(verbose_name="Url completa de instagram", blank=True, null=True)
    show_instagram_button = models.BooleanField(default=True, verbose_name="Mostrar botón instagram", blank=True, null=True)
    youtube = models.URLField(verbose_name="Url completa de youtube", blank=True, null=True)
    show_youtube_button = models.BooleanField(default=True, verbose_name="Mostrar botón youtube", blank=True, null=True)
    tiktok = models.URLField(verbose_name="Url completa de tiktok", blank=True, null=True)
    show_tiktok_button = models.BooleanField(default=True, verbose_name="Mostrar botón tiktok", blank=True, null=True)
    twitterx = models.URLField(verbose_name="Url completa de x/twitter", blank=True, null=True)
    show_twitterx_button = models.BooleanField(default=True, verbose_name="Mostrar botón x/twitter", blank=True, null=True)
    telegram = models.URLField(verbose_name="Url completa de telegram", blank=True, null=True)
    show_telegram_button = models.BooleanField(default=True, verbose_name="Mostrar botón telegram", blank=True, null=True)
    

    show_phone_call = models.BooleanField(default=True, verbose_name="Mostrar botón llamar", blank=True, null=True)
    social_media = models.JSONField(verbose_name="Redes Sociales. Utilizar formato {'facebook':'https://www.facebook.com/tuempresa','instagram':'https://...etc'}", blank=True, null=True)  # Ej: {"facebook": "url", "instagram": "url"}

class Product(models.Model):
    business = models.ForeignKey(BusinessProfile, on_delete=models.CASCADE, related_name="products")
    name = models.CharField(max_length=255, verbose_name="Nombre del Producto")
    description = models.TextField(verbose_name="Descripción del Producto", blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio", blank=True, null=True)
    offer_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio en oferta", blank=True, null=True)
    available = models.BooleanField(default=True, verbose_name="Disponible")
    offer = models.BooleanField(default=False, verbose_name="¿En oferta?",blank=True, null=True)
    image = models.ImageField(upload_to="products/", verbose_name="Imagen", blank=True, null=True)
    product_image1_url = models.URLField(verbose_name="Imagen1 del producto", blank=True, null=True)
    product_image2_url = models.URLField(verbose_name="Imagen2 del producto", blank=True, null=True)
    product_image3_url = models.URLField(verbose_name="Imagen3 del producto", blank=True, null=True)

    product_url = models.URLField(verbose_name="Url del producto", blank=True, null=True)

    def get_product_info(self):
        """
        Devuelve la información completa del producto en un formato legible.
        """
        return f"""
        Producto:
        - Nombre: {self.name if self.name else "No disponible"}
        - Descripción: {self.description if self.description else "No disponible"}
        - Precio: {self.price if self.price is not None else "No disponible"}€
        - Precio en oferta: {self.offer_price if self.offer_price is not None else "No disponible"}€
        - Disponible: {"Sí" if self.available else "No"}
        - En oferta: {"Sí" if self.offer else "No"}
        - Imagen: {self.image.url if self.image else "No disponible"}
        - URL del producto: {self.product_url if self.product_url else "No disponible"}
        """
    def __str__(self):
        return self.name if self.name else "Producto sin nombre"

class Service(models.Model):
    business = models.ForeignKey(BusinessProfile, on_delete=models.CASCADE, related_name="services")
    name = models.CharField(max_length=255, verbose_name="Nombre del Servicio")
    description = models.TextField(verbose_name="Descripción del Servicio", blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio", blank=True, null=True)
    offer_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio en oferta", blank=True, null=True)
    #duration = models.DurationField(verbose_name="Duración Aproximada", blank=True, null=True)
    available = models.BooleanField(default=True, verbose_name="Disponible")
    offer = models.BooleanField(default=False, verbose_name="¿En oferta?", blank=True, null=True)
    image = models.ImageField(upload_to="services/", verbose_name="Imagen", blank=True, null=True)
    service_image1_url = models.URLField(verbose_name="Imagen1 del servicio", blank=True, null=True)
    service_image2_url = models.URLField(verbose_name="Imagen2 del servicio", blank=True, null=True)
    service_image3_url = models.URLField(verbose_name="Imagen3 del servicio", blank=True, null=True)
    service_url = models.URLField(verbose_name="Url del servicio", blank=True, null=True)

    def get_service_info(self):
        """
        Devuelve la información completa del servicio en un formato legible.
        """
        return f"""
        Servicio:
        - Nombre: {self.name if self.name else "No disponible"}
        - Descripción: {self.description if self.description else "No disponible"}
        - Precio: {self.price if self.price is not None else "No disponible"}€
        - Precio en oferta: {self.offer_price if self.offer_price is not None else "No disponible"}€
        - Disponible: {"Sí" if self.available else "No"}
        - En oferta: {"Sí" if self.offer else "No"}
        - Imagen: {self.image.url if self.image else "No disponible"}
        - URL del servicio: {self.service_url if self.service_url else "No disponible"}
        """

    def __str__(self):
        return self.name if self.name else "Servicio sin nombre"
    
class FAQ(models.Model):
    business = models.ForeignKey(BusinessProfile, on_delete=models.CASCADE, related_name="faqs")
    question = models.TextField(verbose_name="Pregunta Frecuente")
    answer = models.TextField(verbose_name="Respuesta")

class Promotion(models.Model):
    business = models.ForeignKey(BusinessProfile, on_delete=models.CASCADE, related_name="promotions")
    title = models.CharField(max_length=255, verbose_name="Título de la Promoción")
    description = models.TextField(verbose_name="Descripción de la Promoción")
    discount = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Descuento (%)", blank=True, null=True)
    valid_until = models.DateField(verbose_name="Válido Hasta", blank=True, null=True)

class CustomResponses(models.Model):
    business = models.ForeignKey(BusinessProfile, on_delete=models.CASCADE, related_name="custom_responses")
    keyword = models.CharField(max_length=255, verbose_name="Palabra Clave")
    response = models.TextField(verbose_name="Respuesta del Asistente")
