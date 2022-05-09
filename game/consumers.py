import json
from game.models import Game
import random
import string
from django.core import serializers
from channels.generic.websocket import AsyncWebsocketConsumer


class NotificationConsumer(AsyncWebsocketConsumer):
    async def websocket_connect(self, event):
        self.group_name = 'notification'

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def websocket_disconnect(self, event):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def websocket_receive(self, text_data):
        received_data = json.loads(text_data['text'])
        method = received_data['method']
        message = received_data['message']
        username = received_data['username']
        lobby = received_data['lobby']
        letterpair = received_data['letterpair']
        wordIsValid = received_data['wordIsValid']
        status = None
        added = False
        try:
            status = await Game.objects.async_get(lobby=lobby)
        except Game.DoesNotExist:
            players = {
                username: 3
            }
            letterpair = ''.join(random.sample(string.ascii_lowercase, 2))
            await Game.objects.async_create(lobby=lobby, players=json.dumps(players), finished=False, winner='Poka hz', letterpair=letterpair)
            status = await Game.objects.async_get(lobby=lobby)
            added = True
            print('created new game instance')
        statusDict = json.loads(status.players)
        if not added:
            statusDict[username] = 3
            await Game.update_(json.dumps(statusDict), status)
            letterpair = status.letterpair
        if not message or not username:
            return False
        if method == 'JOIN':
            response = {
                'type': 'send_message',
                'method': 'JOIN',
                'message': '1337',
                'username': username,
                'lobby': lobby,
                'letterpair': letterpair,
                'wordIsValid': wordIsValid,
                'status': json.dumps(statusDict),
                'move': 'none'
            }
            await self.channel_layer.group_send(self.group_name, response)
            return
        elif method == 'PLAY':
            ind = 0

            for key, value in statusDict.items():
                if key == username:
                    if not wordIsValid:
                        value -= 1
                    break
                ind += 1
            dict_list = list(statusDict.items())
            next_user = None
            if ind + 1 == len(dict_list):
                next_user = dict_list[0][0]
            else:
                next_user = dict_list[ind + 1][0]
            response = {
                'type': 'send_message',
                'method': 'PLAY',
                'message': message,
                'username': username,
                'lobby': lobby,
                'letterpair': letterpair,
                'wordIsValid': wordIsValid,
                'status': json.dumps(statusDict),
                'move': next_user
            }
            await self.channel_layer.group_send(self.group_name, response)
            return
        # print('receivesuccess', event, json.dumps(response))
        # await self.channel_layer.group_send(self.group_name, response)

    async def send_message(self, event):
        print('send_message 1337')
        method = event['method']
        message = event['message']
        username = event['username']
        lobby = event['lobby']
        status = event['status']
        move = event['move']
        letterpair = event['letterpair']
        wordIsValid = event['wordIsValid']
        await self.send(text_data=json.dumps(
            {'method': method, 'message': message, 'username': username, 'lobby': lobby, 'status': status, 'move': move, 'letterpair': letterpair,
             'wordIsValid': wordIsValid}))
