from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .models import *
from django.views.generic.edit import CreateView
from .forms import *
from django.views.generic import *
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login
from django.contrib.auth.views import PasswordChangeView
from .models import Room, Message, CustomUser
from django.utils.crypto import get_random_string
def user_profile(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
            if form.is_valid():
                form.save()
        else:
            form = CustomUserChangeForm(instance=request.user)

        form = CustomUserChangeForm(instance=request.user)
        return render(request, 'profile_reset.html', {'form': form})
    else:
        return redirect('/profile/')

class ChangePassView(PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('game:profile')


def guest(request):
    if request.user.is_authenticated:
        print('redirected')
        return render(request, 'user_page.html')
    else:
        return render(request, 'guest.html')

class ProfileView(TemplateView):
    template_name = "user_page.html"


class ProfileChangeView(FormView):
    form_class = CustomUserChangeForm
    template_name = "profile_reset.html"
    success_url = reverse_lazy('game:profile')


def login_page(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('game:profile')
    else:
        form = AuthenticationForm
    return render(request, 'login.html', {'form':form})
def scoreboard(request):
    users = CustomUser.objects.all()
    return render(request, 'scoreboard.html', {'users': users})
def room(request, room):
    username = request.GET.get('username')
    if request.user.is_authenticated:
        username = request.user.username
    if username == None:
        username = get_random_string(length=10)
    room_details = Room.objects.get(name=room)
    userId = -1

    if(request.user.is_authenticated):
        userId = request.user.id

    return render(request, 'room.html', {
        'username': username,
        'room': room,
        'room_details': room_details,
        'userId': userId
    })

def join(request):
    if request.user.is_authenticated:
        user = request.user.username
        return render(request, 'join.html', {'user': user})

    return render(request, 'join.html')
def public_rooms(request):
    public_rooms = Room.objects.filter(public=True)
    return render(request, 'public_games.html', {'public_rooms': public_rooms})
def room_creation(request):
    if request.user.is_authenticated:
        user = request.user.username
        return render(request, 'create_room.html', {'user': user})

    return render(request, 'create_room.html')
def create_room(request):
    room = request.POST['room_name']
    is_public = request.POST.get('is_public', '') == 'on'
    username = request.POST['username']

    print(room)
    print(username)

    if Room.objects.filter(name=room).exists():
        print('exists')
    else:
        new_room = Room.objects.create(name=room, public=is_public)
        new_room.save()
        return redirect('room/'+room+'/?username='+username)
def join_room(request):
    room = request.POST['room_name']
    username = request.POST['username']

    print(room)
    print(username)

    if Room.objects.filter(name=room).exists():
        return redirect('room/'+room+'/?username='+username)
    else:
        print('nothing')

class registerView(CreateView):
    form_class = CustomUserForm
    success_url = reverse_lazy('login')
    template_name = 'register.html'
