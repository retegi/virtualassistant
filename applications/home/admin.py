from django.contrib import admin
from .models import CustomerProfile

class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "subscription_type", "subscription_start", "subscription_end")
    list_filter = ("subscription_type",)
    search_fields = ("user__username", "user__email")
    ordering = ("user",)
    readonly_fields = ("user",)

    fieldsets = (
        ("Información del Usuario", {
            "fields": ("user",)
        }),
        ("Detalles de la Suscripción", {
            "fields": ("subscription_type", "subscription_start", "subscription_end")
        }),
    )

admin.site.register(CustomerProfile, CustomerProfileAdmin)
# Register your models here.
