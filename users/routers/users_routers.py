from rest_framework.routers import DefaultRouter
from ..viewsets.users_viewsets import *

router = DefaultRouter()

router.register('users', RegisterView , basename = 'RegisterView')
