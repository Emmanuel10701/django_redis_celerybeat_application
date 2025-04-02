from django.urls import re_path
from .consumer import StoryConsumer

websocket_urlpatterns = [
    re_path(r'ws/story/$', StoryConsumer.as_asgi()),
]