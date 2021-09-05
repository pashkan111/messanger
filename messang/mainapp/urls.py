from django.urls import path
from .views import home, room, chat

urlpatterns = [
    path('', home),
    path('room/<str:room_name>', room),
    path('chat', chat),
]
