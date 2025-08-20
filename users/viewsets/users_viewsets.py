from django.contrib.auth import get_user_model, authenticate, login
from rest_framework import generics, viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from ..serializers.users_serializers import RegisterSerializer, UserSerializer, UpdateMeSerializer
from ..permissions.users_permissions import IsAdmin, IsAgent

User = get_user_model()

class RegisterView(viewsets.ViewSet):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

class MeView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def patch(self, request, *args, **kwargs):
        ser = UpdateMeSerializer(self.get_object(), data=request.data, partial=True)
        ser.is_valid(raise_exception=True)
        ser.save()
        return Response(UserSerializer(self.get_object()).data)

class UserViewSet(mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):
    queryset = User.objects.all().order_by("id")
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAgent]

    def get_queryset(self):
        qs = super().get_queryset()
        role = self.request.query_params.get("role")
        if role:
            qs = qs.filter(role=role.upper())
        return qs

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated, IsAdmin])
    def set_role(self, request, pk=None):
        user = self.get_object()
        role = request.data.get("role", "").upper()
        if role not in [r[0] for r in User.Roles.choices]:
            return Response({"detail": "Invalid role."}, status=400)
        user.role = role
        user.save()
        return Response(UserSerializer(user).data)

    @action(detail=False, methods=["post"], permission_classes=[IsAuthenticated])
    def toggle_online(self, request):
        me = request.user
        me.is_online = not me.is_online
        me.save()
        return Response({"is_online": me.is_online})

class SessionLoginView(generics.GenericAPIView):
    """
    Optional: establishes a Django session for WebSocket auth via AuthMiddlewareStack.
    Use only if you want browser cookie-based session auth for Channels.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(request, username=username, password=password)
        if not user:
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
        login(request, user)
        return Response({"detail": "Logged in with session."})
