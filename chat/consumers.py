import json
import re
from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from . import tasks
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
        result = []
        text_data_json = json.loads(text_data)
        action = text_data_json['action']

        if action == 'new_message':
            message = {'username': text_data_json['username'],
                       'message': text_data_json['message']
                       }
            if len(text_data_json['message']) > 0:
                match = re.search(r'^/' + "stock" + '=.*([^\s]+)', text_data_json['message'])
                if not match:
                    if text_data_json['message'].startswith('/'):
                        message = {
                            'username': 'bot',
                            'message': "Invalid code format, should be as follow: /stock=stock_code"
                            }
                        content = {
                            'action': 'new_message',
                            'message': message
                        }
                        await self.send_message(content)
                    else:
                        await self.save_message(text_data_json)
                        await self.channel_layer.group_send(
                            self.room_group_name,
                            {
                                'type': 'chatroom_message',
                                'message': message,
                                'action': "new_message"
                            }
                        )
                else:
                    self.stock_request(match)
        elif action == 'fetch_messages':
            result = await self.fetch_messages()
            content = {
                'action': 'messages',
                'messages': result
            }
            await self.send_message(content)

    async def chatroom_message(self, event):
        """Send messages to the chat room"""
        message = event['message']
        # username = event['username']

        await self.send(text_data=json.dumps({
            'message': message,
            # 'username': username,
            'action': "new_message"
        }))

    async def send_message(self, message):
        """Send a message to the user"""
        await self.send(text_data=json.dumps(message))

    @database_sync_to_async
    def fetch_messages(self):
        result = []
        room_id = Room.objects.get(name=self.room_name).id
        messages = Message.objects.filter(room=room_id).order_by('timestamp')[:50]
        # the async context doesn't allow to fetch the relations of the models
        for item in messages:
            # room_name = Room.objects.get(pk=item.room_id)
            author = User.objects.get(pk=item.author_id).username
            item_message = self.message2json(item, author)
            result.append(item_message)
        return result

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

    def message2json(self, message, author):
        """
        Conver a message into  a dict object
        """
        return {
            'id': message.id,
            'username': author,
            'message': message.body,
            'timestamp': str(message.timestamp)
        }

    def stock_request(self, match):
        tasks.stocksBot.delay(match.group(0)[7:], self.room_group_name)
        # /stock=aapl.us

    async def message_from_task(self, event):
        await self.send(text_data=json.dumps(event))
