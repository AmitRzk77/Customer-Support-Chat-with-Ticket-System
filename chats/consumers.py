# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from .models import ChatRoom, Message
from tickets.models import Ticket

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.ticket_id = self.scope["url_route"]["kwargs"]["ticket_id"]
        self.room_group_name = f"chat_ticket_{self.ticket_id}"

        # Join the group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave the group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        """Receive message from WebSocket and broadcast to the group"""
        data = json.loads(text_data)
        message = data.get("message", "").strip()
        if not message:
            return

        user = self.scope["user"]
        if not user.is_authenticated:
            return  # Ignore anonymous users

        # Save the message in DB
        await self.save_message(user, self.ticket_id, message)

        # Broadcast message to all participants in the group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "username": user.username,
            }
        )

    async def chat_message(self, event):
        """Receive message from group and send to WebSocket"""
        await self.send(text_data=json.dumps({
            "message": event["message"],
            "username": event["username"],
        }))

    @database_sync_to_async
    def save_message(self, user, ticket_id, message):
        """Save message and ensure participants are added"""
        ticket = Ticket.objects.get(id=ticket_id)

        # Get or create chat room linked to this ticket
        room, created = ChatRoom.objects.get_or_create(
            name=f"ticket_{ticket.id}",
            ticket=ticket
        )

        # Add participants if not already
        room.participants.add(ticket.customer)
        if hasattr(ticket, "assigned_agent") and ticket.assigned_agent:
            room.participants.add(ticket.assigned_agent)

        # Only allow participants to send messages
        if user not in room.participants.all():
            return None

        # Create and return message
        return Message.objects.create(room=room, sender=user, content=message)
