from django.contrib.auth import get_user_model
from django.db import models


class Room(models.Model):
    room_name = models.TextField(max_length=100)

    def __str__(self):
        return self.room_name
