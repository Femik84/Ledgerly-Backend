from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import CustomUser
from .serializers import (
    UserSerializer,
    UserCreateSerializer,
    UserUpdateSerializer,
)


class UserViewSet(viewsets.ModelViewSet):
    """
    A viewset for CRUD operations on CustomUser.
    Nested transactions are included when retrieving a single user.
    """

    queryset = CustomUser.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        """Pick serializer based on action."""
        if self.action == "create":
            return UserCreateSerializer
        elif self.action in ["update", "partial_update"]:
            return UserUpdateSerializer
        elif self.action == "retrieve":
            # return full serializer with nested transactions
            return UserSerializer
        return UserSerializer  # optionally, use a simpler serializer for 'list'

    def get_permissions(self):
        """Custom permissions: anyone can register, others need auth."""
        if self.action == "create":
            return [AllowAny()]
        return super().get_permissions()
