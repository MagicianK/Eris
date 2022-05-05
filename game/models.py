from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
class CustomUser(AbstractUser):

    # field to store user picture
    user_avatar = models.ImageField(upload_to="user_avatars", default='NULL')

    # returning username when called
    def __str__(self) -> str:
        return self.username


class Game(models.Model):
    room_name = models.CharField(max_length=100)
    creator = models.CharField(max_length=50, default='NULL')
    number = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.room_name


class TrackPlayers(models.Model):
    username = models.CharField(max_length=50)
    room = models.ForeignKey(Game, on_delete=models.CASCADE)
