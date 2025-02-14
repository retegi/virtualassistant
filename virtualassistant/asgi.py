"""
ASGI config for virtualassistant project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'virtualassistant.settings')

application = get_asgi_application()


from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from applications.assistant.urls import websocket_urlpatterns



os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'virtualassistant.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # Manejo de solicitudes HTTP
    "websocket": AuthMiddlewareStack(  # Manejo de solicitudes WebSocket
        URLRouter(websocket_urlpatterns)  # Incluye las rutas WebSocket
    ),
})