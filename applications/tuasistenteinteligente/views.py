from django.shortcuts import render
from django.http import JsonResponse
import openai
from django.conf import settings
import os

MAX_HISTORY = 20  # Máximo número de mensajes en el historial

def chat_view(request):
    return render(request, 'home/chat.html')

def load_instructions():
    instructions_path = os.path.join(settings.BASE_DIR, 'applications', 'tuasistenteinteligente', 'indications', 'instructions.txt')
    try:
        with open(instructions_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        return "Eres un asistente virtual amigable y útil."

def get_bot_response(request):
    if request.method == 'POST':
        user_message = request.POST.get('message', '')
        openai.api_key = settings.OPENAI_API_KEY

        # Carga las instrucciones desde el archivo
        instructions = load_instructions()

        # Obtener el historial de la sesión
        conversation_history = request.session.get('conversation_history', [])

        # Agregar el mensaje del usuario al historial
        conversation_history.append({"role": "user", "content": user_message})

        # Limitar el historial al máximo definido
        if len(conversation_history) > MAX_HISTORY:
            conversation_history = conversation_history[-MAX_HISTORY:]

        try:
            # Incluir las instrucciones como el primer mensaje en el historial
            messages = [{"role": "system", "content": instructions}] + conversation_history

            # Enviar el historial completo al modelo
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages
            )

            bot_reply = response['choices'][0]['message']['content']

            # Agregar la respuesta del bot al historial
            conversation_history.append({"role": "assistant", "content": bot_reply})

            # Guardar el historial actualizado en la sesión
            request.session['conversation_history'] = conversation_history

            return JsonResponse({'reply': bot_reply})
        except Exception as e:
            print(f"Error con OpenAI: {e}")  # Depuración
            return JsonResponse({'error': str(e)})

    return JsonResponse({'error': 'Invalid request'})

def end_conversation(request):
    if 'conversation_history' in request.session:
        del request.session['conversation_history']
    return JsonResponse({'status': 'Conversación finalizada'})
