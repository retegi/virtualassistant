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
from applications.home.models import SubscriptionType, CustomerProfile





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



class AssistantInstructionBuilder:
    def __init__(self, assistant_url_name):
        self.business_profile = get_object_or_404(BusinessProfile, assistant_url_name=assistant_url_name)
        self.customer_profile = get_object_or_404(CustomerProfile, user=self.business_profile.user)

    def get_products(self):
        if self.has_premium_access():
            products = Product.objects.filter(business=self.business_profile)
            return "\n".join(p.get_product_info() for p in products) if products.exists() else "No hay productos disponibles."
        return "No disponible en la versión gratuita."

    def get_services(self):
        if self.has_premium_access():
            services = Service.objects.filter(business=self.business_profile)
            return "\n".join(s.get_service_info() for s in services) if services.exists() else "No hay servicios disponibles."
        return "No disponible en la versión gratuita."

    def get_faqs(self):
        if self.has_premium_access():
            faqs = FAQ.objects.filter(business=self.business_profile)
            return "\n".join(f"Pregunta: {f.question}\nRespuesta: {f.answer}" for f in faqs) if faqs.exists() else "No hay preguntas frecuentes disponibles."
        return "No disponible en la versión gratuita."

    def has_premium_access(self):
        return self.customer_profile.subscription_type in [
            SubscriptionType.PREMIUM_MONTHLY, 
            SubscriptionType.PREMIUM_ANNUAL
        ]

    def build(self):
        bp = self.business_profile
        return f"""
Eres un asistente virtual de la empresa {bp.company_name or "No disponible"}.
Tu objetivo es proporcionar información sobre la empresa, sus productos, servicios y preguntas frecuentes a los clientes.

🔹 **Importante**: 
- Si la respuesta incluye una imagen, debes devolver solo la URL completa de la imagen con etiquetas HTML <img src="" class="w-50"> para mostrar la imagen, sin ningún texto adicional ni formato Markdown.
- Si la respuesta incluye un enlace o url, debe devolver código con con etiqueta HTML <a href="" target="_blank">.
- El sistema mostrará automáticamente las imágenes y los enlaces en el chat.

Información de la empresa:
- Nombre: {bp.company_name or "No disponible"}
- Mostrar nombre: {"Sí" if bp.show_company_name else "No"}
- Descripción: {bp.description or "No disponible"}
- Contacto: {bp.contact_email or "No disponible"}, Teléfono: {bp.phone or "No disponible"}
- Web: {bp.website or "No disponible"}
- Dirección: {bp.address or "No disponible"}
- Horario: {json.dumps(bp.business_hours, indent=4, ensure_ascii=False) if bp.business_hours else "No disponible"}
- Redes Sociales: {json.dumps(bp.social_media, indent=4, ensure_ascii=False) if bp.social_media else "No disponible"}

Personalización visual:
- Imagen asistente: {bp.assistant_image.url if bp.assistant_image else "No disponible"}
- Mostrar imagen: {"Sí" if bp.show_assistant_image else "No"}
- Imagen fondo: {bp.background_image.url if bp.background_image else "No disponible"}
- Colores: fondo {bp.background_color}, formulario {bp.form_background_color}, botón {bp.button_background_color}, texto botón {bp.button_text_color}, cliente {bp.chat_customer_text_color}, asistente {bp.chat_assistant_text_color}

Configuración:
- URL asistente: {bp.assistant_url_name or "No disponible"}
- Logo empresa: {bp.company_logo.url if bp.company_logo else "No disponible"}
- Mostrar logo: {"Sí" if bp.show_company_logo else "No"}

Productos:
{self.get_products()}

Servicios:
{self.get_services()}

Preguntas frecuentes:
{self.get_faqs()}

Responde a las preguntas de los clientes basándote en esta información.
        """

# Uso:
def load_instructions(assistant_url_name):
    builder = AssistantInstructionBuilder(assistant_url_name)
    return builder.build()




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

        except openai.error.OpenAIError as e:
            print(f"🔥 ERROR en OpenAI: {e}")
            return JsonResponse({'error': f"OpenAI Error: {str(e)}"}, status=500)

        except json.JSONDecodeError:
            print("🔥 ERROR: JSON inválido en la solicitud")
            return JsonResponse({'error': 'Error en el formato JSON'}, status=400)

        except Exception as e:
            print(f"🔥 ERROR inesperado en get_bot_response: {e}")
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
