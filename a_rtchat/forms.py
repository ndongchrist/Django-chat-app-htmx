from django import forms
from django.forms import ModelForm
from a_rtchat.models import *


class ChatMessageForm(ModelForm):
    class Meta:
        model = ChatMessage
        fields = ['body']       
        widgets = {
            'body': forms.TextInput(attrs={'placeholder': 'Add message ...', 'maxlength': '150', 'class': 'p-4 text_black', 'max-lenght': '300', 'autofocus': True}),
        }