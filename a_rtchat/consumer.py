import json
from channels.generic.websocket import WebsocketConsumer
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from a_rtchat.models import ChatGroup, ChatMessage
from asgiref.sync import async_to_sync

class ChatRoomConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope['user']
        self.chatroom_name = self.scope['url_route']['kwargs']['chatroom_name']
        self.chat_group = get_object_or_404(ChatGroup, group_name=self.chatroom_name)
        
        async_to_sync(self.channel_layer.group_add)(
            self.chatroom_name, 
            self.channel_name)
        
        #add and update user online
        if self.user not in self.chat_group.users_online.all():
            self.chat_group.users_online.add(self.user)
            self.update_online_count()
        
        self.accept()
        
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['body']
        print('hello')
        
        message = ChatMessage.objects.create(
            body=message, 
            author=self.user, 
            group=self.chat_group)
        
        # self.send(text_data=html)
        event = {
            'type': 'message_handler',
            'message_id': message.id,
        }
        
        async_to_sync(self.channel_layer.group_send)(
            self.chatroom_name, 
            event
        )
        
        
    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.chatroom_name, 
            self.channel_name
        )  
        
        #remove user from online list
        if self.user in self.chat_group.users_online.all():
            self.chat_group.users_online.remove(self.user)  
            self.update_online_count()
        
        
    def message_handler(self, event):
        message_id = event['message_id']
        message = get_object_or_404(ChatMessage, id=message_id)
        context = {
            'message': message,
            'user': self.user,
        }
        html = render_to_string('a_rtchat/partials/chat_message_p.html', context)
        self.send(text_data=html)
        
        
    def update_online_count(self):
        online_count = self.chat_group.users_online.count() - 1
        
        event = {
                'type': 'online_count_handler',
                'online_count': online_count,
            }
        
        async_to_sync(self.channel_layer.group_send)(
            self.chatroom_name, 
            event
        )
        
    def online_count_handler(self, event):
        online_count = event['online_count']
        
        context = {
            'online_count': online_count,
        }
        print(online_count)
        html = render_to_string('a_rtchat/partials/online_count.html', context)
        self.send(text_data=html)