from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .models import *
from django.views.generic.edit import CreateView
from .forms import *
from django.views.generic import *
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login


def guest(request):
    return render(request, 'guest.html')

class ProfileView(TemplateView):
    template_name = "user_page.html"

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
