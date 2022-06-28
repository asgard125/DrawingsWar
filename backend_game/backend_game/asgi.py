"""
ASGI config for backend_game project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os
from battle_app.middleware import TokenAuthMiddleware
from channels.routing import ProtocolTypeRouter, URLRouter, ChannelNameRouter
from django.core.asgi import get_asgi_application
from channels.security.websocket import AllowedHostsOriginValidator
from battle_app.consumers import EngineConsumer, PlayerConsumer
import battle_app.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_game.settings')

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
  "http": django_asgi_app,
  "websocket": TokenAuthMiddleware(
            URLRouter(
                battle_app.routing.websocket_urlpatterns
        )
    ),
    "channel": ChannelNameRouter({"game_engine": EngineConsumer.as_asgi()}),
})
