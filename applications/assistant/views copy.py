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

    # Construir listas de productos y servicios formateados
    product_list = "\n".join(
        [f"- {p.name}: {p.description or 'Sin descripción'}, Precio: {p.price}€" for p in products]
    ) if products else "No hay productos disponibles."

    service_list = "\n".join(
        [f"- {s.name}: {s.description or 'Sin descripción'}, Precio: {s.price}€, Duración: {s.duration}" for s in services]
    ) if services else "No hay servicios disponibles."

    # Construir la información del asistente
    instructions = f"""
    Eres un asistente virtual de la empresa {business_profile.company_name}. 
    Tu objetivo es proporcionar información sobre la empresa, sus productos y servicios a los clientes.

    Información de la empresa:
    - Descripción: {business_profile.description or "No disponible"}
    - Contacto: {business_profile.contact_email or "No disponible"}, Teléfono: {business_profile.phone or "No disponible"}
    - Dirección: {business_profile.address or "No disponible"}
    - Horario de atención: {business_profile.business_hours or "No disponible"}
    - Redes Sociales: {business_profile.social_media or "No disponible"}

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
