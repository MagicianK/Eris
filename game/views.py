from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .models import *
from django.views.generic.edit import CreateView
from .forms import *
from django.contrib import messages
from django.utils.crypto import get_random_string
from django.views.generic import *
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login
from django.contrib.auth.views import PasswordChangeView


def user_profile(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = CustomUserChangeForm(request.POST, instance=request.user)
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


class registerView(CreateView):
    form_class = CustomUserForm
    success_url = reverse_lazy('login')
    template_name = 'register.html'


def room(request, room_name):
    game = Game.objects.get(room_name=room_name)

    print(game)

    creator = game.creator

    print(creator)

    number = game.number

    return render(request, 'play.html', {
        'room': room_name,
        'creator': creator,
        'number': number,
    })


def createRoom(request):
    creator = request.user.get_username()

    if request.method == "POST":
        number = request.POST.get('option')

        if number is not None:
            room_name = get_random_string(length=50)
            game = Game(room_name=room_name, creator=creator, number=number)
            game.save()

            print(number)
            print(creator)
            print(room_name)

            print("/game/" + room_name + "/")

            return redirect("/game/" + room_name + "/")

    return render(request, 'create_room.html')


def joinRoom(request):

    if request.method == "POST":
        username = request.POST.get('username')
        room_name = request.POST.get('room_name')

        print(username)
        print(room_name)

        if username is not None:
            if room_name is not None:

                game = Game.objects.get(room_name=room_name)

                if game is not None:

                    messages.success(request, username)
                    return redirect("/game/" + room_name + "/")

    return render(request, 'join_room.html')

