from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
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
        return UserSerializer  # default

    def get_permissions(self):
        """Custom permissions: anyone can register, others need auth."""
        if self.action == "create":
            return [AllowAny()]
        if self.action == "me":
            return [IsAuthenticated()]
        return super().get_permissions()

    @action(detail=False, methods=["get"], url_path="me")
    def me(self, request):
        """
        Get the currently authenticated user's profile.
        """
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(serializer.data)
