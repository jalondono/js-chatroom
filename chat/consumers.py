import json
import re
from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Room, Message
from django.contrib.auth import get_user_model

User = get_user_model()


class ChatRoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = text_data_json['username']
        action = text_data_json['action']
        if action == 'new_message':
            await self.save_message(text_data_json)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chatroom_message',
                    'message': message,
                    'username': username,
                }
            )
        elif action == 'fetch_messages':
            await self.fetch_messages

    async def chatroom_message(self, event):
        message = event['message']
        username = event['username']

        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
        }))

    @database_sync_to_async
    def fetch_messages(self, data):
        result = []
        messages = Message.objects.filter(room=self.room_name).order_by('-timestamp')[:50]
        for item in messages:
            result.append(self.message2json(item))

    @database_sync_to_async
    def save_message(self, data):
        room_obj = (Room.objects.filter(name=self.room_name).first())
        author = data['username']
        author_user = (User.objects.filter(username=author).first())
        body_message = data['message']
        message = (Message.objects.create(
            author=author_user,
            body=body_message,
            room=room_obj
        ))

    def message2json(self, message):
        """
        Conver a message into  a dict object
        """
        return {
            'id': message.id,
            'author': message.author.username,
            'body': message.body,
            'timestamp': str(message.timestamp)
        }
