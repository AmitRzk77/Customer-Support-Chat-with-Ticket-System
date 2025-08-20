# chat/serializers.py
from rest_framework import serializers
from ..models import Message

class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Message
        fields = ('id', 'room', 'sender', 'content', 'timestamp')
