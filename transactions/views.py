from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Transaction
from .serializers import (
    TransactionSerializer,
    TransactionCreateSerializer,
    TransactionUpdateSerializer,
)


class TransactionViewSet(viewsets.ModelViewSet):
    """
    A viewset for CRUD operations on transactions.
    """

    permission_classes = [IsAuthenticated]
    queryset = Transaction.objects.all()

    def get_queryset(self):
        """
        Users can only see their own transactions.
        """
        user = self.request.user
        return Transaction.objects.filter(user=user).order_by("-date", "-created_at")

    def get_serializer_class(self):
        """
        Choose serializer based on action.
        """
        if self.action == "create":
            return TransactionCreateSerializer
        elif self.action in ["update", "partial_update"]:
            return TransactionUpdateSerializer
        return TransactionSerializer
