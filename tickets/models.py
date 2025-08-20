# tickets/models.py
from django.conf import settings
from django.db import models

class Ticket(models.Model):
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tickets'
    )
    assigned_agent = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='assigned_tickets',
        null=True,
        blank=True
    )
    subject = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=50, default='Open')  # Open, Pending, Closed
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.subject} - {self.customer.username}"
