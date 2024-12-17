from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from a_rtchat.models import *
from .forms import *

# Create your views here.
@login_required
def chat_View(request):
    chat_group = get_object_or_404(ChatGroup, group_name='public_chat')
    chat_messages = chat_group.chat_messages.all()[:30]
    form = ChatMessageForm()
    
    if request.htmx:
        form = ChatMessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.author = request.user
            message.group = chat_group
            message.save()
            context = {
                'message': message,
                'user': request.user,
            }
            return render(request, 'a_rtchat/partials/chat_message_p.html', context)
    context = {
        'chat_messages': chat_messages,
        'form': form,
    }
    return render(request, 'a_rtchat/chat.html', context)


@login_required
def get_or_create_chatroom(request, username):
    if request.user.username == username:
        return redirect('home')
    
    other_user = get_object_or_404(User, username=username)
    my_chatrooms = ChatGroup.objects.filter(members=request.user) 