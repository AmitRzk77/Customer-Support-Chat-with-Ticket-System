from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

# Import your routers
from chats.routers.chats_routers import router as chats_router
from users.routers.users_routers import router as users_router
from tickets.routers.tickets_router import router as tickets_router

# Combine all routers
router = routers.DefaultRouter()
router.registry.extend(chats_router.registry)
router.registry.extend(users_router.registry)
router.registry.extend(tickets_router.registry)

urlpatterns = [
    # Admin site
    path('admin/', admin.site.urls),

    # API routes
    path('api/', include(router.urls)),

    # App URLs
    path('tickets/', include('tickets.urls')),
    path('chats/', include('chats.urls')),
    

    # Account URLs (handles customer/admin login/logout)
    path('account/', include('account.urls')),
]
