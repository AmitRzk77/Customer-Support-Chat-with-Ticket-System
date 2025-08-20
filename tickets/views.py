
from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Ticket

@login_required
def ticket_chat(request):
    return render(request, "ticket_chat.html")

def is_admin(user):
    return user.is_staff

@login_required
@user_passes_test(is_admin)
def admin_ticket_list(request):
    tickets = Ticket.objects.all()
    return render(request, 'ticket_list.html', {'tickets': tickets})

def chatroom(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    return render(request, "chat_rooms.html", {"ticket": ticket})

