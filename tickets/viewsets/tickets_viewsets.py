from rest_framework import viewsets, permissions
from ..models import Ticket
from ..serializers.tickets_serializers import TicketSerializer

class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated]


    def get_queryset(self):
     user = self.request.user
     if user.is_staff:  # Admin
        return Ticket.objects.all()
     return Ticket.objects.filter(customer=user)  # Customer only sees own

