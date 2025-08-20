from rest_framework.routers import DefaultRouter
from ..viewsets.chats_viewsets import ChatHistoryView
from django.urls import re_path
from .. import consumers

router = DefaultRouter()

router.register('chats', ChatHistoryView, basename = 'ChatHistoryView')

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<ticket_id>\d+)/$', consumers.ChatConsumer.as_asgi()),
]