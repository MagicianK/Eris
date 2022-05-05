import json
from channels.generic.websocket import AsyncWebsocketConsumer


class NotificationConsumer(AsyncWebsocketConsumer):
    async def websocket_connect(self, event):
        self.group_name = 'notification'

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def websocket_disconnect(self, event):
        await self.channel_layer.group_discard(self.group_name, self.channel_name )

    async def websocket_receive(self, text_data):
        received_data = json.loads(text_data['text'])
        message = received_data['message']
        username = received_data['username']

        if not message or not username:
            return False

        response = {
            'type': 'send_message',
            'message': message,
            'username': username
        }

        # print('receivesuccess', event, json.dumps(response))

        await self.channel_layer.group_send(self.group_name, response)

    async def send_message(self, event):
        message = event['message']
        username = event['username']

        await self.send(text_data=json.dumps({'message': message, 'username': username}))
