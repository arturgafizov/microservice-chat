import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .services import AsyncChatService


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Join room group

        print('user-data', self.scope['user_data'])
        self.user = self.scope['user_data']
        await self.init_user_chat()
        await self.accept()

    async def init_user_chat(self):
        self.chats: list = await AsyncChatService.get_chat_ids(self.user['id'])
        # print(chats)
        for chat in self.chats:
            await self.channel_layer.group_add(str(chat), self.channel_name)

    async def disconnect(self, close_code):
        # Leave room group
        pass
        # await self.channel_layer.group_discard(
        #     self.room_group_name,
        #     self.channel_name
        # )

    # Receive message from WebSocket
    async def receive_json(self, data: dict, **kwargs):
        print('receive_json', data, kwargs)
        # text_data_json = json.loads(data)
        # message = text_data_json['message']

        # Send message to room group
        # await self.channel_layer.group_send(
        #     self.room_group_name,
        #     {
        #         'type': 'chat_message',
        #         'message': message
        #     }
        # )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
