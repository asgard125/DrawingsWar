from django.urls import re_path
from rest_framework.authtoken.models import Token
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/battle/(?P<room_name>\w+)/$', consumers.PlayerConsumer.as_asgi()),
]