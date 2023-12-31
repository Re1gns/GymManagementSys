"""
ASGI config for GymManagementSystem project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from channels.security.websocket import AllowedHostsOriginValidator
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from django.urls import path
import main.routing
import main.consumers  # Assuming your consumers module is in the main app

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GymManagementSystem.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    'websocket': AllowedHostsOriginValidator(
            AuthMiddlewareStack(URLRouter(main.routing.ws_patterns))
        ),
})
