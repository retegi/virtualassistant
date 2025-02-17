from django.urls import include, path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import get_bot_response


app_name = 'assistant_app'

urlpatterns = [
    path('',
        views.BusinessProfileCreateView.as_view(),
        name='create_assistant',
    ),
    path('',
        views.WebAssistantView.as_view(),
        name='web_assistant',
    ),
    path('api/get_response/', views.get_bot_response, name='get_bot_response'),
    path('end_conversation/', views.end_conversation, name='end_conversation'),
    path("chat/", get_bot_response, name="chat_view"),  # Asegúrate de que esta línea esté presente
    path("<str:assistant_url_name>/chat_api/", get_bot_response, name="chat_api"), 

]