# chats/models.py
from django.db import models
from django.conf import settings
from tickets.models import Ticket

class ChatRoom(models.Model):
    ticket = models.OneToOneField(
        Ticket,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='chatroom'
    )
    name = models.CharField(max_length=255)
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='chatrooms'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def add_participants(self):
        if self.ticket:
            self.participants.add(self.ticket.customer)
            if hasattr(self.ticket, 'assigned_agent') and self.ticket.assigned_agent:
                self.participants.add(self.ticket.assigned_agent)

    def __str__(self):
        return f"{self.name} ({self.ticket})" if self.ticket else self.name

class Message(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username}: {self.content[:20]}"