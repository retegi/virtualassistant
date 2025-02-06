from django.db import models
from django.contrib.auth.models import User

class BusinessProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="business_profile")
    company_name = models.CharField(max_length=255, verbose_name="Nombre de la Empresa")
    assistant_url_name = models.CharField(max_length=255, verbose_name="Nombre url")
    description = models.TextField(verbose_name="Descripción de la Empresa", blank=True, null=True)
    contact_email = models.EmailField(verbose_name="Correo Electrónico de Contacto", blank=True, null=True)
    phone = models.CharField(max_length=20, verbose_name="Teléfono", blank=True, null=True)
    website = models.URLField(verbose_name="Sitio Web", blank=True, null=True)
    address = models.TextField(verbose_name="Dirección", blank=True, null=True)
    business_hours = models.JSONField(verbose_name="Horario de Atención", blank=True, null=True)  # Guardado como JSON
    social_media = models.JSONField(verbose_name="Redes Sociales", blank=True, null=True)  # Ej: {"facebook": "url", "instagram": "url"}

class Product(models.Model):
    business = models.ForeignKey(BusinessProfile, on_delete=models.CASCADE, related_name="products")
    name = models.CharField(max_length=255, verbose_name="Nombre del Producto")
    description = models.TextField(verbose_name="Descripción del Producto", blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio", blank=True, null=True)
    available = models.BooleanField(default=True, verbose_name="Disponible")
    image = models.ImageField(upload_to="products/", verbose_name="Imagen", blank=True, null=True)

class Service(models.Model):
    business = models.ForeignKey(BusinessProfile, on_delete=models.CASCADE, related_name="services")
    name = models.CharField(max_length=255, verbose_name="Nombre del Servicio")
    description = models.TextField(verbose_name="Descripción del Servicio", blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio", blank=True, null=True)
    duration = models.DurationField(verbose_name="Duración Aproximada", blank=True, null=True)
    available = models.BooleanField(default=True, verbose_name="Disponible")

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
