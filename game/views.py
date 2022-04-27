from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .models import *
from django.views.generic.edit import CreateView
from .forms import *
from django.views.generic import *
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login
from django.contrib.auth.views import PasswordChangeView


class ChangePassView(PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('game:profile')


def guest(request):
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
