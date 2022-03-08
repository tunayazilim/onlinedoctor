"""
ASGI config for config project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

from channels.routing import ProtocolTypeRouter
from django.core.asgi import get_asgi_application
import django
from channels.http import AsgiHandler
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import chat.routing


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')





application = get_asgi_application()

ws_pattern = []

application = ProtocolTypeRouter({
    #"https": get_asgi_application(),  aslında http yazıyor ama öyle çalışmıyor https yapınca çalışıyor
    "websocket" : AuthMiddlewareStack(URLRouter(
        chat.routing.websocket_urlpatterns
    ))
})


