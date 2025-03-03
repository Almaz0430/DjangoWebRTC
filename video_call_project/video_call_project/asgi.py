"""
ASGI config for video_call_project project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path
from video_calls.consumers import VideoCallConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'video_call_project.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter([
            path('ws/video/<str:room_id>/', VideoCallConsumer.as_asgi()),
        ])
    ),
})
