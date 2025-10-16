from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import UserDevice

class UserDeviceViewSet(viewsets.ModelViewSet):
    """
    Manage user devices / FCM tokens.
    """
    queryset = UserDevice.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Return devices for current user
        return UserDevice.objects.filter(user=self.request.user)

    @action(detail=False, methods=["post"], url_path="register-token")
    def register_token(self, request):
        """
        Register or update a device token.
        Expected payload: { "fcm_token": "...", "device_name": "optional" }
        """
        token = request.data.get("fcm_token")
        device_name = request.data.get("device_name", "")

        if not token:
            return Response(
                {"error": "fcm_token is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Avoid duplicate tokens
        device, created = UserDevice.objects.update_or_create(
            user=request.user,
            fcm_token=token,
            defaults={"device_name": device_name},
        )

        return Response(
            {"message": "Device registered successfully.", "created": created},
            status=status.HTTP_200_OK
        )
