import shortuuid

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class ChatGroup(models.Model):
    group_name = models.CharField(max_length=100, unique=True, default=shortuuid.uuid)
    users_online = models.ManyToManyField(User, related_name='users_online')
    description = models.TextField()
    members = models.ManyToManyField(User, related_name='members', blank=True)
    is_private = models.BooleanField(default=False)
    
    def __str__(self):
        return self.group_name

class ChatMessage(models.Model):
    body = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    group = models.ForeignKey(ChatGroup, on_delete=models.CASCADE, related_name='chat_messages', null=True, blank=True)
    
    def __str__(self):      
        return f'{self.author.username} says {self.body}'
    
    class Meta:
        ordering = ['-created']