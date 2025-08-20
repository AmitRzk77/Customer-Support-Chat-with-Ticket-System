from celery import shared_task
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from .models import Ticket

User = get_user_model()

@shared_task
def send_ticket_email(ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)
    subject = f'Ticket Update: {ticket.subject}'
    message = f'Hello {ticket.customer.username},\n\nYour ticket status is: {ticket.status}'
    
    send_mail(
        subject,
        message,
        'support@livehelp.com',
        [ticket.customer.email],
        fail_silently=False,
    )
