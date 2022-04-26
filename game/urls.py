from django.urls import path
from .views import *
from game import views
from django.contrib.auth.views import auth_login
from django.contrib.auth import views as auth_views
# app name to use in pairs with urls in templates
app_name = 'game'

# url patterns that gives us resources when requested
# structure is path(string_url, view_name, name=url_name)
urlpatterns = [
    # index (main) page
    path('', views.guest, name='guest'),
    path('login/', views.login_page, name="login_page"),
    path('', views.login, name="login"),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/change/', ProfileChangeView.as_view(), name='profile_change'),
    path('profile/password/', ChangePassView.as_view(template_name='password_reset.html'), name='password_change'),
    # localhost:8000/register
    path("register/", registerView.as_view(), name="registration"),
]
