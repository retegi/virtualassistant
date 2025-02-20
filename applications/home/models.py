from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

# Create your models here.
class SubscriptionType(models.TextChoices):
    FREE = "free", _("Gratis")
    PREMIUM_MONTHLY = "premium_monthly", _("Premium Mensual")
    PREMIUM_ANNUAL = "premium_annual", _("Premium Anual")

class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="customer_profile")
    subscription_type = models.CharField(
        max_length=20,
        choices=SubscriptionType.choices,
        default=SubscriptionType.FREE
    )
    subscription_start = models.DateTimeField(null=True, blank=True)
    subscription_end = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.get_subscription_type_display()}"