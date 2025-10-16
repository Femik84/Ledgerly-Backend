from rest_framework import viewsets, status
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
    Includes endpoint for updating Firebase push notification token.
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
            return UserSerializer
        return UserSerializer  # default

    def get_permissions(self):
        """Custom permissions: anyone can register, others need auth."""
        if self.action == "create":
            return [AllowAny()]
        if self.action in ["me", "update_firebase_token"]:
            return [IsAuthenticated()]
        return super().get_permissions()

    @action(detail=False, methods=["get"], url_path="me")
    def me(self, request):
        """Return the authenticated user's profile."""
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(serializer.data)

    # ✅ NEW: endpoint for saving Firebase Cloud Messaging token
    @action(detail=False, methods=["post"], url_path="update-firebase-token")
    def update_firebase_token(self, request):
        """
        Save or update the Firebase Cloud Messaging (FCM) token for the current user.
        Expected payload: { "firebase_notification_token": "your_fcm_token_here" }
        """
        token = request.data.get("firebase_notification_token")

        if not token:
            return Response(
                {"error": "firebase_notification_token is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Save token to current user
        user = request.user
        user.firebase_notification_token = token
        user.save(update_fields=["firebase_notification_token"])

        return Response(
            {"message": "Firebase notification token updated successfully."},
            status=status.HTTP_200_OK,
        )
