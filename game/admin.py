from django.contrib import admin
from game.models import *

from .models import Room, Message

admin.site.register(CustomUser)
admin.site.register(Room)
admin.site.register(Message)

# Register your models here.
