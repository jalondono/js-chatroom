from django.urls import path
from . import views

app_name = 'chat'
urlpatterns = [
    path('select/', views.select_room, name='select'),
    path('select/<str:room_name>/', views.chat_room, name='room'),
]
