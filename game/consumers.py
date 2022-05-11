import json
from game.models import Game
import random
import string
from django.core import serializers
from channels.generic.websocket import AsyncWebsocketConsumer


class NotificationConsumer(AsyncWebsocketConsumer):

    def check_for_result(self, statusDict, roundsDict):
        sum = 0
        for key, value in statusDict.items():
            sum += min(1, value)
        lst = -1


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
            rounds = {
                username: 0
            }
            letterpair = ''.join(random.sample(string.ascii_lowercase, 2))

            await Game.objects.async_create(lobby=lobby
                                            , players=json.dumps(players)
                                            , rounds=json.dumps(rounds)
                                            , finished=False
                                            , winner='Poka hz'
                                            , letterpair=letterpair)

            status = await Game.objects.async_get(lobby=lobby)
            added = True
            print('created new game instance')
        statusDict = json.loads(status.players)
        roundsDict = json.loads(status.rounds)
        if not message or not username:
            return False
        if method == 'JOIN':
            if not added:
                statusDict[username] = 3
                await Game.update_players(json.dumps(statusDict), status)
                letterpair = status.letterpair

                roundsDict[username] = 0
                await Game.update_rounds(json.dumps(roundsDict), status)
            response = {
                'type': 'send_message',
                'method': 'JOIN',
                'message': '1337',
                'username': username,
                'lobby': lobby,
                'letterpair': letterpair,
                'wordIsValid': wordIsValid,
                'status': json.dumps(statusDict),
                'move': 'none',
                'last': 'none'
            }
            await self.channel_layer.group_send(self.group_name, response)
            return
        elif method == 'PLAY':
            roundsDict[username] = roundsDict[username]+1
            await Game.update_rounds(json.dumps(roundsDict), status)
            if not wordIsValid:
                statusDict[username] = statusDict[username]-1
                await Game.update_players(json.dumps(statusDict), status)
                self.check_for_result(statusDict, roundsDict)

            await Game.update_letterpair(''.join(random.sample(string.ascii_lowercase, 2)), status)
            letterpair = status.letterpair

            response = {
                'type': 'send_message',
                'method': 'PLAY',
                'message': message,
                'username': username,
                'lobby': lobby,
                'letterpair': letterpair,
                'wordIsValid': wordIsValid,
                'status': json.dumps(statusDict),
                'move': '1337',
                'last': 'none'
            }
            await self.channel_layer.group_send(self.group_name, response)

            ind = 0

            for key, value in statusDict.items():
                if key == username:
                    if not wordIsValid:
                        value -= 1
                    break
                ind += 1
            dict_list = list(statusDict.items())
            next_user = None
            last_user = None

            if ind + 1 == len(dict_list):
                next_user = dict_list[0][0]

                for items in dict_list:
                    if items[1] == 0:
                        dict_list.remove(items)

                if len(dict_list) == 1:
                    last_user = dict_list[0][0]
                    next_user = None

            else:
                next_user = dict_list[ind + 1][0]

            response = {
                'type': 'send_message',
                'method': 'MOVE',
                'message': '1337',
                'username': username,
                'lobby': lobby,
                'letterpair': letterpair,
                'wordIsValid': '1337',
                'status': json.dumps(statusDict),
                'move': next_user,
                'last': last_user
            }
            await self.channel_layer.group_send(self.group_name, response)
            return
        elif method == 'START':
            dict_list = list(statusDict.items())
            next_user = dict_list[0][0]
            response = {
                'type': 'send_message',
                'method': 'MOVE',
                'message': '1337',
                'username': username,
                'lobby': lobby,
                'letterpair': letterpair,
                'wordIsValid': '1337',
                'status': json.dumps(statusDict),
                'move': next_user,
                'last': 'none'
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
        last = event['last']
        letterpair = event['letterpair']
        wordIsValid = event['wordIsValid']
        await self.send(text_data=json.dumps(
            {'method': method, 'message': message, 'username': username, 'lobby': lobby, 'status': status, 'move': move, 'last': last, 'letterpair': letterpair,
             'wordIsValid': wordIsValid}))
