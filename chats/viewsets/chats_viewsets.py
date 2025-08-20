from rest_framework import  viewsets
from rest_framework.response import Response
from ..models import ChatRoom
from ..serializers.chats_serializers import MessageSerializer

class ChatHistoryView(viewsets.ViewSet):
    def get(self, request, room_name):
        room, created = ChatRoom.objects.get_or_create(name=room_name)
        messages = room.messages.all().order_by('timestamp')
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)
