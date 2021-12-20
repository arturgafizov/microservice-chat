from collections import namedtuple
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from .services import AsyncChatService
from main.models import UserData


class ChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        # Join room group

        print('user-data', self.scope['user_data'])
        self.user: UserData = self.scope['user_data']
        await self.init_user_chat()
        await self.accept()

    async def init_user_chat(self):
        self.chats: list = await AsyncChatService.get_chat_ids(self.user.id)
        # print(self.chats)
        for chat in self.chats:
            await self.channel_layer.group_add(str(chat), self.channel_name)
            await self.channel_layer.group_send(str(chat),
                {
                    'type': 'user_status',
                    'response': {
                        'command': 'user_status',
                        'online': True,
                        'user_id': self.user.id,
                        'chat_id': str(chat),
                    },
                }
                                                )

    async def disconnect(self, close_code):
        # Leave room group

        for chat in self.chats:
            await self.channel_layer.group_discard(str(chat), self.channel_name)

    async def new_message(self, data):
        # print('new message', data)
        message = await AsyncChatService.save_message(self.user.id, data['message'], data['chat_id'])
        # print(message)
        response: dict = {
            'command': 'new_message',
            'author_id': message.author_id,
            'chat_id': message.chat_id,
            'content': message.content,
            'avatar': self.user.avatar_url,
            'date': message.date.strftime('%H:%M'),
        }
        await self.channel_layer.group_send(
            message.chat_id,
            {
                'type': 'chat_message',
                'response': response,
            }
        )

    async def write_message(self, data):
        print('write message', data)

    command = {
        'new_message': new_message,
        'write_message': write_message,
    }

    # Receive message from WebSocket
    async def receive_json(self, data: dict, **kwargs):
        await self.command[data['command']](self, data)

        # Send message to room group

    # Receive message from room group
    async def chat_message(self, event):
        print('event', event)
        data: dict = event['response']
        #
        # # Send message to WebSocket
        await self.send_json(data)

    async def user_status(self, event: dict):
        data: dict = event['response']
        await self.send_json(data)
