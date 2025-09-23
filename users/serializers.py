from rest_framework import serializers
from .models import CustomUser
from transactions.serializers import TransactionSerializer  # import your transaction serializer


class UserSerializer(serializers.ModelSerializer):
    """Serializer for reading/updating user objects with nested transactions."""

    transactions = TransactionSerializer(many=True, read_only=True)  # nested transactions

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "email",
            "name",
            "image",
            "date_joined",
            "balance",
            "income_total",
            "expense_total",
            "transactions",  # include nested transactions
        ]
        read_only_fields = [
            "id",
            "date_joined",
            "balance",
            "income_total",
            "expense_total",
            "transactions",
        ]


class UserCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating new users with password + image required."""

    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "email",
            "name",
            "password",
            "image",
            "date_joined",
            "balance",
            "income_total",
            "expense_total",
        ]
        read_only_fields = ["id", "date_joined", "balance", "income_total", "expense_total"]

    def validate_image(self, value):
        if not value:
            raise serializers.ValidationError("Profile image is required.")
        return value

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = CustomUser.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating user profile (excluding email)."""

    class Meta:
        model = CustomUser
        fields = ["name", "image", "balance", "income_total", "expense_total"]
