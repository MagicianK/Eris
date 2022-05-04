from django.urls import path
from .views import *
from game import views
from django.contrib.auth.views import auth_login
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

# app name to use in pairs with urls in templates
app_name = 'game'

# url patterns that gives us resources when requested
# structure is path(string_url, view_name, name=url_name)
urlpatterns = [
    # index (main) page login_required(ProfileChangeView.as_view(), login_url='/login/')
    path('', views.guest, name='guest'),
    path('login/', views.login_page, name="login_page"),
    path('', views.login, name="login"),
    path('profile/', login_required(ProfileView.as_view(), login_url='/login/'), name='profile'),
    path('profile/change/', views.user_profile, name='profile_change'),
    path('profile/password/', login_required(ChangePassView.as_view(template_name='password_reset.html'), login_url='/login/'), name='password_change'),
    # localhost:8000/register
    path("register/", registerView.as_view(), name="registration"),


    #game

    path('game/<str:room_name>/', views.room, name='room_name'),
    path('game/create/room/', views.createRoom, name='create_room'),
    path('join/game/', views.joinRoom, name='join_room'),

    #path("game/")
]
