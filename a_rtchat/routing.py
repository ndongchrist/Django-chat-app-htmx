# chat/routing.py
from django.urls import path

from .consumer import *

websocket_urlpatterns = [
    path(r"ws/chatroom/<chatroom_name>", ChatRoomConsumer.as_asgi()),
]