# livehelp/asgi.py
import os
import django
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'livehelp.settings')
django.setup()  # Ensure Django apps are loaded

# Import your routing
import chats.routers.chats_routers
# ASGI application
application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # Handles normal HTTP requests
    "websocket": AuthMiddlewareStack(
        URLRouter(
            chats.routers.chats_routers.websocket_urlpatterns
        )
    ),
})
