from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ..viewsets.tickets_viewsets import TicketViewSet

router = DefaultRouter()
router.register('tickets', TicketViewSet, basename='ticket')

# urlpatterns = [
#     path('api/', include(router.urls)),
# ]
