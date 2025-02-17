from django.urls import path
from . import views
from .views import get_bot_response


urlpatterns = [
    #path('chat/', views.chat_view, name='chat_view'),
    path('api/get_response/', views.get_bot_response, name='get_bot_response'),
    path('end_conversation/', views.end_conversation, name='end_conversation'),
    path("chat/", get_bot_response, name="chat_view"),  # Asegúrate de que esta línea esté presente
    path("<str:assistant_url_name>/chat_api/", get_bot_response, name="chat_api"), 
]