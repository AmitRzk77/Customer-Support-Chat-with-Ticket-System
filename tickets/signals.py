# tickets/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Ticket
from chats.models import ChatRoom

@receiver(post_save, sender=Ticket)
def create_chat_room(sender, instance, created, **kwargs):
    if created:
        room_name = f"ticket_{instance.id}"
        room, _ = ChatRoom.objects.get_or_create(name=room_name, ticket=instance)
        room.participants.add(instance.customer)
        if hasattr(instance, "assigned_agent") and instance.assigned_agent:
            room.participants.add(instance.assigned_agent)
