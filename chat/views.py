from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from . import forms
from .models import Room


# Create your views here.

@login_required(login_url="/accounts/login/")
def chat_room(request, room_name):
    if not Room.objects.filter(name=room_name).first():
        Room.objects.create(name=room_name)
    return render(request, 'chat/chatroom.html', {'room_name': room_name})


@login_required(login_url="/accounts/login/")
def select_room(request):
    if request.method == 'POST':
        form = forms.SelectRoom(request.POST)
        if form.is_valid():
            return redirect('chat:room', room_name=form.data['name'])
    else:
        form = forms.SelectRoom()
    return render(request, 'chat/selectroom.html', {'form': form})
