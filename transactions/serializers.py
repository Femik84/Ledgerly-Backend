from rest_framework import serializers
from .models import Transaction
from category.models import Category


class TransactionSerializer(serializers.ModelSerializer):
    """Serializer for reading transaction details."""

    category_name = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = Transaction
        fields = [
            "id",
            "user",
            "type",
            "category",
            "category_name",
            "amount",
            "title",       
            "date",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "user", "created_at", "updated_at", "category_name"]

    def to_representation(self, instance):
        """Customize output to include category name."""
        rep = super().to_representation(instance)
        rep["category_name"] = instance.category.name if instance.category else None
        return rep


class TransactionCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating transactions. User is set automatically."""

    class Meta:
        model = Transaction
        fields = ["type", "category", "amount", "title", "date"]  # updated

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than 0.")
        return value

    def create(self, validated_data):
        user = self.context["request"].user
        transaction = Transaction.objects.create(user=user, **validated_data)
        return transaction


class TransactionUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating transactions."""

    class Meta:
        model = Transaction
        fields = ["type", "category", "amount", "title", "date"]  # updated

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than 0.")
        return value
