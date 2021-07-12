from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Room(models.Model):
    name = models.TextField(max_length=100)

    def __str__(self):
        return self.name


class Message(models.Model):
    room = models.ForeignKey('chat.Room', models.CASCADE)
    author = models.ForeignKey(
        User, related_name='user_messages', on_delete=models.CASCADE)
    body = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
