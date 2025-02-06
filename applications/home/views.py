from django.shortcuts import render
from django.views.generic import (
    TemplateView,
    CreateView,
    UpdateView,
)
from applications.assistant.models import BusinessProfile, Product, Service, FAQ, Promotion, CustomResponses
from applications.assistant.forms import BusinessProfileForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy


from django.views.generic.edit import CreateView

class HomePageView(CreateView):
    model = BusinessProfile
    form_class = BusinessProfileForm
    template_name = "home/index.html"

    def form_valid(self, form):
        # Asignar el usuario actual al perfil antes de guardarlo
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("home_app:tarifa")  # Redirigir a la página de tarifas



class TarifaPageView(TemplateView):
    template_name='home/tarifa.html'

