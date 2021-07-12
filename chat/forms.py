from django import forms
from . import models


class SelectRoom(forms.ModelForm):
    class Meta:
        model = models.Room
        fields = ['room_name']
