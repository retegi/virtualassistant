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
from django.http import JsonResponse
import openai
from django.conf import settings
import json
from applications.assistant.models import BusinessProfile, Product, Service





class BusinessProfileCreateView(CreateView):
    model = BusinessProfile
    form_class = BusinessProfileForm
    template_name = "assistant/business_profile_form.html"
    
    def get_object(self):
        return self.request.user.business_profile  # Obtener perfil del usuario actual

    def get_success_url(self):
        return reverse_lazy("perfil_actualizado")
    

class BusinessProfileUpdateView(UpdateView):
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



MAX_HISTORY = 20  # Máximo número de mensajes en el historial

def chat_view(request):
    return render(request, 'home/chat.html')

def load_instructions(assistant_url_name):
    """
    Carga las instrucciones del asistente basado en el BusinessProfile asociado al assistant_url_name.
    """
    # Obtener el perfil de negocio
    business_profile = get_object_or_404(BusinessProfile, assistant_url_name=assistant_url_name)

    # Obtener productos y servicios relacionados
    products = Product.objects.filter(business=business_profile)
    services = Service.objects.filter(business=business_profile)

    # Construcción detallada de la lista de productos
    product_list = "\n".join([
        p.get_product_info() for p in products
    ]) if products.exists() else "No hay productos disponibles."

    # Construcción detallada de la lista de servicios
    service_list = "\n".join([
        s.get_service_info() for s in services
    ]) if services.exists() else "No hay servicios disponibles."

    # Construcción detallada de la información del asistente
    instructions = f"""
    Eres un asistente virtual de la empresa {business_profile.company_name if business_profile.company_name else "No disponible"}.
    Tu objetivo es proporcionar información sobre la empresa, sus productos y servicios a los clientes.

    🔹 **Importante**: 
    - Si la respuesta incluye una imagen, debes devolver solo la URL completa de la imagen, sin ningún texto adicional ni formato Markdown.
    - Si la respuesta incluye un enlace, solo devuelve la URL completa.
    - El sistema mostrará automáticamente las imágenes y los enlaces en el chat.

    Información de la empresa:
    - Nombre de la empresa: {business_profile.company_name if business_profile.company_name else "No disponible"}
    - Mostrar nombre: {"Sí" if business_profile.show_company_name else "No"}
    - Descripción: {business_profile.description if business_profile.description else "No disponible"}
    - Contacto: {business_profile.contact_email if business_profile.contact_email else "No disponible"}, 
      Teléfono: {business_profile.phone if business_profile.phone else "No disponible"}
    - Sitio Web: {business_profile.website if business_profile.website else "No disponible"}
    - Dirección: {business_profile.address if business_profile.address else "No disponible"}
    - Horario de atención: {json.dumps(business_profile.business_hours, indent=4, ensure_ascii=False) if business_profile.business_hours else "No disponible"}
    - Redes Sociales: {json.dumps(business_profile.social_media, indent=4, ensure_ascii=False) if business_profile.social_media else "No disponible"}

    Personalización visual:
    - Imagen del asistente: {business_profile.assistant_image.url if business_profile.assistant_image else "No disponible"}
    - Mostrar imagen del asistente: {"Sí" if business_profile.show_assistant_image else "No"}
    - Imagen de fondo: {business_profile.background_image.url if business_profile.background_image else "No disponible"}
    - Color de fondo de la página: {business_profile.background_color if business_profile.background_color else "No disponible"}
    - Color de fondo del formulario: {business_profile.form_background_color if business_profile.form_background_color else "No disponible"}
    - Color de fondo del botón: {business_profile.button_background_color if business_profile.button_background_color else "No disponible"}
    - Color de texto del botón: {business_profile.button_text_color if business_profile.button_text_color else "No disponible"}
    - Color de texto del chat del cliente: {business_profile.chat_customer_text_color if business_profile.chat_customer_text_color else "No disponible"}
    - Color de texto del chat del asistente: {business_profile.chat_assistant_text_color if business_profile.chat_assistant_text_color else "No disponible"}

    Configuración del asistente:
    - Nombre URL del asistente: {business_profile.assistant_url_name if business_profile.assistant_url_name else "No disponible"}
    - Logo de empresa: {business_profile.company_logo.url if business_profile.company_logo else "No disponible"}
    - Mostrar logo de empresa: {"Sí" if business_profile.show_company_logo else "No"}

    Productos disponibles:
    {product_list}

    Servicios ofrecidos:
    {service_list}

    Responde a las preguntas de los clientes basándote en esta información.
    """

    return instructions


def get_bot_response(request, assistant_url_name):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '')

            print(f"📩 Mensaje recibido: {user_message}")

            # Obtener información específica del asistente
            instructions = load_instructions(assistant_url_name)

            # Configurar API Key correctamente
            openai.api_key = settings.OPENAI_API_KEY

            # Realizar la consulta a OpenAI con la versión correcta
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": instructions},
                    {"role": "user", "content": user_message}
                ]
            )

            bot_reply = response['choices'][0]['message']['content']

            print(f"🤖 Respuesta de OpenAI: {bot_reply}")

            return JsonResponse({'reply': bot_reply})

        except Exception as e:
            print(f"🔥 ERROR en get_bot_response: {e}")
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request'}, status=400)

def end_conversation(request):
    if 'conversation_history' in request.session:
        del request.session['conversation_history']
    return JsonResponse({'status': 'Conversación finalizada'})

def assistant_view(request, assistant_url_name):
    # Buscar el perfil de negocio basado en la URL
    business_profile = get_object_or_404(BusinessProfile, assistant_url_name=assistant_url_name)

    context = {
        'business_profile': business_profile,
    }

    return render(request, 'assistant/assistant_chat.html', context)
