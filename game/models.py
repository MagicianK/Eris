from django.db import models
from datetime import datetime
from channels.db import database_sync_to_async

# Create your models here.
from django.contrib.auth.models import AbstractUser
from random import randint
from asgiref.sync import sync_to_async
class CustomUser(AbstractUser):
    # field to store user picture
    user_avatar = models.ImageField(upload_to="user_avatars", default=f'user_avatars/profimg/DEFAULT_{randint(1, 13)}.png')
    score = models.IntegerField(default=0)
    # returning username when called
    def __str__(self) -> str:
        return self.username
    @database_sync_to_async
    def update_score(self, user, score):
        user.score = score
        user.save()

class Room(models.Model):
    name = models.CharField(max_length=50)
    public = models.BooleanField(default=True)

class Message(models.Model):
    value = models.CharField(max_length=500)
    date = models.DateTimeField(default=datetime.now, blank=True)
    room = models.CharField(max_length=100000)
    user = models.CharField(max_length=100000)


class Game(models.Model):
    lobby = models.CharField(max_length=5000)
    players = models.TextField(max_length=100000, default='{}')
    rounds = models.TextField(max_length=100000, default='{}')
    finished = models.BooleanField(default=False)
    winner = models.CharField(max_length=5000)
    letterpair = models.CharField(max_length=2, default='xx')
    @database_sync_to_async
    def update_players(self, players, status):
        status.players = players
        status.save()
    @database_sync_to_async
    def update_rounds(self, rounds, status):
        status.rounds = rounds
        status.save()
    @database_sync_to_async
    def update_letterpair(self, letterpair, status):
        status.letterpair = letterpair
        status.save()
    @database_sync_to_async
    def update_gameStatus(self, winner, status):
        status.winner = winner
        status.finished = True
        status.save()
