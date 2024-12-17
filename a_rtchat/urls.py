from django.urls import path
from a_rtchat.views import *

urlpatterns = [
    path('', chat_View, name="home"),  
    path('chat/<chatroom_name>/', get_or_create_chatroom, name="start-chat"),
]