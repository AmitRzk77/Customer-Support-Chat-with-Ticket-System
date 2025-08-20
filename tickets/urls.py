from django.urls import path, include
from .views import ticket_chat
from .import views


urlpatterns = [
    path("ticket-chat/", ticket_chat, name="ticket_chat"),
    path("admin/list/", views.admin_ticket_list, name="admin_ticket_list"),
    path("chat/<int:ticket_id>/", views.chatroom, name="chatroom"),
   
    
]

