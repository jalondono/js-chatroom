from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes

# Create your views here.
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer


# data = {'token': "dfdsfsdf545ds4f5"}
# valid_data = VerifyJSONWebTokenSerializer().validate(data)
# user = valid_data['user']

def index(request):
    return render(request, 'index.html', {})


@permission_classes([IsAuthenticated])
def room(request, room_name):
    return render(request, 'chatroom.html', {'room_name': room_name})
