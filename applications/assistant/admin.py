from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import BusinessProfile, Product, Service, FAQ, Promotion, CustomResponses

class ProductInline(admin.TabularInline):  # Permite agregar productos dentro del perfil de negocio
    model = Product
    extra = 1

class ServiceInline(admin.TabularInline):  # Permite agregar servicios dentro del perfil de negocio
    model = Service
    extra = 1

class FAQInline(admin.TabularInline):  # Permite agregar preguntas frecuentes dentro del perfil
    model = FAQ
    extra = 1

class PromotionInline(admin.TabularInline):  # Promociones dentro del perfil
    model = Promotion
    extra = 1

class CustomResponsesInline(admin.TabularInline):  # Respuestas personalizadas dentro del perfil
    model = CustomResponses
    extra = 1

@admin.register(BusinessProfile)
class BusinessProfileAdmin(admin.ModelAdmin):
    list_display = ("company_name", "assistant_url_name", "contact_email", "phone", "website")  # Columnas visibles
    search_fields = ("company_name", "assistant_url_name", "contact_email", "phone")  # Campos de búsqueda
    list_filter = ("company_name",)  # Filtros en la barra lateral
    prepopulated_fields = {"assistant_url_name": ("company_name",)}  # Generar URL automáticamente desde el nombre
    inlines = [ProductInline, ServiceInline, FAQInline, PromotionInline, CustomResponsesInline]  # Relacionados en el mismo formulario

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "business", "price", "available")
    search_fields = ("name", "business__company_name")
    list_filter = ("available", "business")

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "business", "price", "available")
    search_fields = ("name", "business__company_name")
    list_filter = ("available", "business")

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ("question", "business")
    search_fields = ("question", "business__company_name")

@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ("title", "business", "discount", "valid_until")
    search_fields = ("title", "business__company_name")
    list_filter = ("valid_until",)

@admin.register(CustomResponses)
class CustomResponsesAdmin(admin.ModelAdmin):
    list_display = ("keyword", "business")
    search_fields = ("keyword", "business__company_name")
