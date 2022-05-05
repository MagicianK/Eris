from django.db import models
from datetime import datetime

# Create your models here.
from django.contrib.auth.models import AbstractUser
class CustomUser(AbstractUser):

    # field to store user picture
    user_avatar = models.ImageField(upload_to="user_avatars", default='NULL')

    # returning username when called
    def __str__(self) -> str:
        return self.username

class Room(models.Model):
    name = models.CharField(max_length=50)
class Message(models.Model):
    value = models.CharField(max_length=500)
    date = models.DateTimeField(default=datetime.now, blank=True)
    room = models.CharField(max_length=100000)
    user = models.CharField(max_length=100000)
