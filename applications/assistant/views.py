from django.shortcuts import render
from django.views.generic import (
    TemplateView,
    CreateView,
    UpdateView,
    DetailView,
)
from .models import BusinessProfile, Product, Service, FAQ, Promotion, CustomResponses
from .forms import BusinessProfileForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404





class BusinessProfileCreateView(CreateView):
    model = BusinessProfile
    form_class = BusinessProfileForm
    template_name = "assistant/business_profile_form.html"
    
    def get_object(self):
        return self.request.user.business_profile  # Obtener perfil del usuario actual

    def get_success_url(self):
        return reverse_lazy("perfil_actualizado")
    

class AssistantDetailView(DetailView):
    model = BusinessProfile
    template_name = "assistant/virtual_assistant.html"
    context_object_name = "datos"

    def get_object(self):
        # Buscar el perfil del negocio basado en assistant_url_name
        return get_object_or_404(BusinessProfile, assistant_url_name=self.kwargs["assistant_url_name"])
    
class WebAssistantView(TemplateView):
    template_name="assistant/virtual_assistant.html"