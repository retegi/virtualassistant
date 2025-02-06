from django.shortcuts import render
from django.views.generic import (
    TemplateView,
    CreateView,
    UpdateView,
)
from .models import BusinessProfile, Product, Service, FAQ, Promotion, CustomResponses
from .forms import BusinessProfileForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy





class BusinessProfileCreateView(CreateView):
    model = BusinessProfile
    form_class = BusinessProfileForm
    template_name = "assistant/business_profile_form.html"
    
    def get_object(self):
        return self.request.user.business_profile  # Obtener perfil del usuario actual

    def get_success_url(self):
        return reverse_lazy("perfil_actualizado")