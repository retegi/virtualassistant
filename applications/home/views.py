from django.shortcuts import render
from django.views.generic import (
    TemplateView,
    CreateView,
    UpdateView,
    DetailView,
    DeleteView,
    FormView,
    ListView,
)
from applications.assistant.models import BusinessProfile, Product, Service, FAQ, Promotion, CustomResponses
from .models import CustomerProfile, SubscriptionType
from applications.assistant.forms import BusinessProfileForm, CompleteBusinessProfileForm, ProductForm, ServiceForm, FAQForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.core.mail import send_mail  # <--- IMPORTANTE
from django.conf import settings
from django.http import JsonResponse

from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
import requests  # <--- IMPORTANTE

from .forms import ContactForm




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





def formulario_contactar(request):
    if request.method == "POST":
        name = request.POST.get("name", "")
        email = request.POST.get("email", "")
        phone = request.POST.get("phone", "")
        company = request.POST.get("company", "")
        message = request.POST.get("message", "")
        recaptcha_response = request.POST.get("g-recaptcha-response")

        # Validar reCAPTCHA con Google
        recaptcha_verify = requests.post(
            "https://www.google.com/recaptcha/api/siteverify",
            data={
                "secret": settings.RECAPTCHA_PRIVATE_KEY,
                "response": recaptcha_response,
            }
        ).json()

        if not recaptcha_verify.get("success"):
            messages.error(request, "Error: reCAPTCHA inválido. Intenta nuevamente.")
            return render(request, "home/index.html", {
                "name": name,
                "email": email,
                "phone": phone,
                "company": company,
                "message": message
            })

        # Enviar correo con los datos ingresados desde la web
        asunto = f"Tu Asistente Inteligente Nuevo mensaje de contacto de {name}"
        contenido = (
            f"Nombre: {name}\n"
            f"Email: {email}\n"
            f"Teléfono: {phone}\n"
            f"Empresa: {company}\n"
            f"Mensaje:\n{message}"
        )

        try:
            send_mail(
                asunto,
                contenido,
                settings.EMAIL_HOST_USER,  # Remitente
                ["euskodev@gmail.com"],  # Cambia por el correo real
                fail_silently=False,
            )
            messages.success(request, "Tu mensaje ha sido enviado con éxito.")
            return redirect("home_app:home")

        except Exception as e:
            messages.error(request, f"Error al enviar el correo: {str(e)}")
            return render(request, "home/index.html", {
                "name": name,
                "email": email,
                "phone": phone,
                "company": company,
                "message": message
            })

    return redirect("home_app:home")



class TarifaPageView(TemplateView):
    template_name='home/tarifa.html'



class TarifaAnualPageView(TemplateView):
    template_name='home/tarifa_anual.html'

class TarifaMensualPageView(TemplateView):
    template_name='home/tarifa_mensual.html'


class DashboardView(TemplateView):
    template_name = 'dashboard/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Obtener el usuario autenticado
        user = self.request.user
        
        # Filtrar los perfiles de negocio por el usuario autenticado
        context['my_assistants'] = BusinessProfile.objects.filter(user=user)
        
        # Obtener el perfil de cliente y la suscripción
        customer_profile = CustomerProfile.objects.filter(user=user).first()
        context['subscription_type'] = customer_profile.subscription_type if customer_profile else "free"

        return context
    
class AssistantProfileDetailView(LoginRequiredMixin, DetailView):
    model = BusinessProfile
    template_name = 'dashboard/assistant_detail.html'
    context_object_name = 'assistant_profile'

    def get_queryset(self):
        """
        Asegura que el usuario autenticado solo pueda ver sus propios perfiles de negocio.
        """
        return BusinessProfile.objects.filter(user=self.request.user)


class AssistantCreateView(LoginRequiredMixin, CreateView):
    model = BusinessProfile
    form_class = CompleteBusinessProfileForm
    template_name = "dashboard/assistant_create.html"
    success_url = reverse_lazy("home_app:dashboard")

    def form_valid(self, form):
        """Asigna automáticamente el usuario autenticado antes de guardar el formulario."""
        form.instance.user = self.request.user
        self.object = form.save()  # Guarda el objeto en self.object antes de redirigir
        return super().form_valid(form)

    def form_invalid(self, form):
        """Evita el error asegurando que self.object esté definido antes de renderizar."""
        self.object = None  # Se asegura de que no haya un objeto antes de renderizar el formulario inválido
        return self.render_to_response(self.get_context_data(form=form))
    

class AssistantUpdateView(LoginRequiredMixin, UpdateView):
    model = BusinessProfile
    form_class = CompleteBusinessProfileForm
    template_name = "dashboard/assistant_create.html"
    success_url = reverse_lazy("home_app:dashboard")

    def form_valid(self, form):
        """Asigna automáticamente el usuario autenticado antes de guardar el formulario."""
        form.instance.user = self.request.user
        self.object = form.save()  # Guarda el objeto en self.object antes de redirigir
        return super().form_valid(form)

    def form_invalid(self, form):
        """Evita el error asegurando que self.object esté definido antes de renderizar."""
        self.object = None  # Se asegura de que no haya un objeto antes de renderizar el formulario inválido
        return self.render_to_response(self.get_context_data(form=form))
    

class AssistantDeleteView(LoginRequiredMixin, DeleteView):
    model = BusinessProfile
    template_name = "dashboard/assistant_confirm_assistant_delete.html"
    success_url = reverse_lazy("home_app:dashboard")

    def get_object(self, queryset=None):
        """
        Asegura que el usuario autenticado solo pueda eliminar su propio BusinessProfile.
        """
        obj = super().get_object(queryset)
        if obj.user != self.request.user:
            raise Http404("No tienes permiso para eliminar este perfil.")
        return obj
    


class CreateProductView(LoginRequiredMixin, FormView):
    template_name = "dashboard/assistant_product_create.html"
    form_class = ProductForm

    def dispatch(self, request, *args, **kwargs):
        """Verifica que el usuario tenga acceso al BusinessProfile especificado en la URL."""
        self.business_profile = get_object_or_404(BusinessProfile, id=kwargs["business_id"], user=request.user)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        """Asocia el producto al BusinessProfile y lo guarda."""
        product = form.save(commit=False)
        product.business = self.business_profile
        product.save()
        
        messages.success(self.request, f"Producto '{product.name}' añadido a {self.business_profile.company_name}.")
        return redirect("home_app:dashboard")  # Redirigir al dashboard después de guardar

class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = "dashboard/assistant_product_list.html"
    context_object_name = "products"
    paginate_by = 10  # Opcional: paginar resultados

    def get_queryset(self):
        """Filtrar productos por el BusinessProfile seleccionado"""
        business_id = self.kwargs.get("business_id")
        business_profile = get_object_or_404(BusinessProfile, id=business_id, user=self.request.user)
        return Product.objects.filter(business=business_profile)

    def get_context_data(self, **kwargs):
        """Agregar el BusinessProfile al contexto para mostrar detalles en la plantilla"""
        context = super().get_context_data(**kwargs)
        context["business_profile"] = get_object_or_404(BusinessProfile, id=self.kwargs.get("business_id"))
        return context
    

class UpdateProductView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "dashboard/assistant_product_update.html"

    def get_object(self, queryset=None):
        """Obtiene el producto solo si pertenece a un BusinessProfile del usuario autenticado."""
        product = get_object_or_404(Product, id=self.kwargs["pk"])
        
        # Verifica que el producto pertenece a un BusinessProfile del usuario autenticado
        if product.business.user != self.request.user:
            messages.error(self.request, "No tienes permiso para editar este producto.")
            return redirect("home_app:dashboard")

        return product

    def form_valid(self, form):
        """Guarda los cambios y redirige al usuario."""
        messages.success(self.request, f"Producto '{form.instance.name}' actualizado correctamente.")
        return super().form_valid(form)

    def get_success_url(self):
        """Redirige a la lista de productos después de la actualización."""
        return reverse_lazy("home_app:product_list", kwargs={"business_id": self.object.business.id})


class DeleteProductView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = "dashboard/assistant_confirm_product_delete.html"

    def get_object(self, queryset=None):
        """Obtiene el producto solo si pertenece a un BusinessProfile del usuario autenticado."""
        product = get_object_or_404(Product, id=self.kwargs["pk"])
        
        # Verifica que el producto pertenece a un BusinessProfile del usuario autenticado
        if product.business.user != self.request.user:
            messages.error(self.request, "No tienes permiso para eliminar este producto.")
            return redirect("home_app:dashboard")

        return product

    def get_success_url(self):
        """Redirige a la lista de productos después de la eliminación."""
        return reverse_lazy("home_app:product_list", kwargs={"business_id": self.object.business.id})

    def delete(self, request, *args, **kwargs):
        """Muestra un mensaje de confirmación tras la eliminación."""
        product = self.get_object()
        messages.success(request, f"Producto '{product.name}' eliminado correctamente.")
        return super().delete(request, *args, **kwargs)
    



#Services:


class CreateServiceView(LoginRequiredMixin, FormView):
    template_name = "dashboard/assistant_service_create.html"
    form_class = ServiceForm

    def dispatch(self, request, *args, **kwargs):
        """Verifica que el usuario tenga acceso al BusinessProfile especificado en la URL."""
        self.business_profile = get_object_or_404(BusinessProfile, id=kwargs["business_id"], user=request.user)
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """Procesa el formulario asegurando que request.FILES esté presente."""
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        """Asocia el servicio al BusinessProfile y lo guarda."""
        service = form.save(commit=False)
        service.business = self.business_profile
        service.save()
        
        messages.success(self.request, f"Servicio '{service.name}' añadido a {self.business_profile.company_name}.")
        return redirect("home_app:dashboard")  # Redirigir al dashboard después de guardar

class ServiceListView(LoginRequiredMixin, ListView):
    model = Service
    template_name = "dashboard/assistant_service_list.html"
    context_object_name = "services"
    paginate_by = 10  # Opcional: paginar resultados

    def get_queryset(self):
        """Filtrar productos por el BusinessProfile seleccionado"""
        business_id = self.kwargs.get("business_id")
        business_profile = get_object_or_404(BusinessProfile, id=business_id, user=self.request.user)
        return Service.objects.filter(business=business_profile)

    def get_context_data(self, **kwargs):
        """Agregar el BusinessProfile al contexto para mostrar detalles en la plantilla"""
        context = super().get_context_data(**kwargs)
        context["business_profile"] = get_object_or_404(BusinessProfile, id=self.kwargs.get("business_id"))
        return context
    

class UpdateServiceView(LoginRequiredMixin, UpdateView):
    model = Service
    form_class = ServiceForm
    template_name = "dashboard/assistant_service_update.html"

    def get_object(self, queryset=None):
        """Obtiene el producto solo si pertenece a un BusinessProfile del usuario autenticado."""
        service = get_object_or_404(Service, id=self.kwargs["pk"])
        
        # Verifica que el producto pertenece a un BusinessProfile del usuario autenticado
        if service.business.user != self.request.user:
            messages.error(self.request, "No tienes permiso para editar este servicio.")
            return redirect("home_app:dashboard")

        return service

    def form_valid(self, form):
        """Guarda los cambios y redirige al usuario."""
        messages.success(self.request, f"Servicio '{form.instance.name}' actualizado correctamente.")
        return super().form_valid(form)

    def get_success_url(self):
        """Redirige a la lista de productos después de la actualización."""
        return reverse_lazy("home_app:service_list", kwargs={"business_id": self.object.business.id})


class DeleteServiceView(LoginRequiredMixin, DeleteView):
    model = Service
    template_name = "dashboard/assistant_confirm_service_delete.html"

    def get_object(self, queryset=None):
        """Obtiene el producto solo si pertenece a un BusinessProfile del usuario autenticado."""
        service = get_object_or_404(Service, id=self.kwargs["pk"])
        
        # Verifica que el producto pertenece a un BusinessProfile del usuario autenticado
        if service.business.user != self.request.user:
            messages.error(self.request, "No tienes permiso para eliminar este servicio.")
            return redirect("home_app:dashboard")

        return service

    def get_success_url(self):
        """Redirige a la lista de productos después de la eliminación."""
        return reverse_lazy("home_app:service_list", kwargs={"business_id": self.object.business.id})

    def delete(self, request, *args, **kwargs):
        """Muestra un mensaje de confirmación tras la eliminación."""
        service = self.get_object()
        messages.success(request, f"Servicio '{service.name}' eliminado correctamente.")
        return super().delete(request, *args, **kwargs)



#FAQ

class FAQListView(LoginRequiredMixin, ListView):
    model = FAQ
    template_name = "dashboard/assistant_faq_list.html"
    context_object_name = "faqs"
    paginate_by = 10  # Opcional: paginar resultados

    def get_queryset(self):
        """Filtrar preguntas frecuentes por el BusinessProfile seleccionado"""
        business_id = self.kwargs.get("business_id")
        business_profile = get_object_or_404(BusinessProfile, id=business_id, user=self.request.user)
        return FAQ.objects.filter(business=business_profile)

    def get_context_data(self, **kwargs):
        """Agregar el BusinessProfile al contexto para mostrar detalles en la plantilla"""
        context = super().get_context_data(**kwargs)
        context["business_profile"] = get_object_or_404(BusinessProfile, id=self.kwargs.get("business_id"))
        return context
    


class FAQCreateView(LoginRequiredMixin, FormView):
    template_name = "dashboard/assistant_faq_create.html"
    form_class = FAQForm

    def dispatch(self, request, *args, **kwargs):
        """Verifica que el usuario tenga acceso al BusinessProfile especificado en la URL."""
        self.business_profile = get_object_or_404(BusinessProfile, id=kwargs["business_id"], user=request.user)
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """Procesa el formulario asegurando que request.FILES esté presente."""
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        """Asocia la pregunta frecuente al BusinessProfile y la guarda."""
        faq = form.save(commit=False)
        faq.business = self.business_profile
        faq.save()
        
        messages.success(self.request, f"Pregunta frecuente añadida a {self.business_profile.company_name}.")
        return redirect("home_app:list_faq")  # Redirigir al dashboard después de guardar
    




class FAQDeleteView(LoginRequiredMixin, DeleteView):
    model = FAQ
    template_name = "dashboard/assistant_confirm_faq_delete.html"

    def get_object(self, queryset=None):
        """Obtiene la pregunta frecuente solo si pertenece a un BusinessProfile del usuario autenticado."""
        faq = get_object_or_404(FAQ, id=self.kwargs["pk"])
        
        # Verifica que la pregunta frecuente pertenece a un BusinessProfile del usuario autenticado
        if faq.business.user != self.request.user:
            messages.error(self.request, "No tienes permiso para eliminar esta pregunta frecuente.")
            return redirect("home_app:list_faq")

        return faq

    def get_success_url(self):
        """Redirige a la lista de preguntas frecuentes después de la eliminación."""
        return reverse_lazy("home_app:list_faq", kwargs={"business_id": self.object.business.id})

    def delete(self, request, *args, **kwargs):
        """Muestra un mensaje de confirmación tras la eliminación."""
        faq = self.get_object()
        messages.success(request, f"Pregunta frecuente eliminada correctamente.")
        return super().delete(request, *args, **kwargs)




class FAQUpdateView(LoginRequiredMixin, UpdateView):
    model = FAQ
    form_class = FAQForm
    template_name = "dashboard/assistant_faq_update.html"

    def get_object(self, queryset=None):
        """Obtiene la pregunta frecuente solo si pertenece a un BusinessProfile del usuario autenticado."""
        faq = get_object_or_404(FAQ, id=self.kwargs["pk"])
        
        # Verifica que la pregunta frecuente pertenece a un BusinessProfile del usuario autenticado
        if faq.business.user != self.request.user:
            messages.error(self.request, "No tienes permiso para editar esta pregunta frecuente.")
            return redirect("home_app:dashboard")

        return faq

    def form_valid(self, form):
        """Guarda los cambios y redirige al usuario."""
        messages.success(self.request, f"Pregunta frecuente actualizada correctamente.")
        return super().form_valid(form)

    def get_success_url(self):
        """Redirige a la lista de preguntas frecuentes después de la actualización."""
        return reverse_lazy("home_app:list_faq", kwargs={"business_id": self.object.business.id})
