from django.db import models, transaction
from django.utils import timezone
from django.conf import settings
from category.models import Category
from budgets.models import Budget   # ✅ import Budget model


class Transaction(models.Model):
    """Transaction model for income and expenses with automatic user balance updates."""

    TYPE_CHOICES = (
        ("income", "Income"),
        ("expense", "Expense"),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="transactions"
    )
    type = models.CharField(max_length=7, choices=TYPE_CHOICES)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="transactions"
    )
    budget = models.ForeignKey(   # ✅ NEW FIELD
        Budget,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="transactions"
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    title = models.CharField(max_length=150, default="Untitled Transaction")
    date = models.DateTimeField(default=timezone.now)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-date", "-created_at"]

    def __str__(self):
        return f"{self.user.email} - {self.type} - {self.amount} ({self.category})"

    # -------------------------
    # Balance auto-update logic
    # -------------------------
    def save(self, *args, **kwargs):
        """Update user totals when creating or updating a transaction."""
        with transaction.atomic():
            if self.pk:  # Updating an existing transaction
                old = Transaction.objects.get(pk=self.pk)
                self._reverse_user_update(old)

            super().save(*args, **kwargs)
            self._apply_user_update()

    def delete(self, *args, **kwargs):
        """Reverse user totals when deleting a transaction."""
        with transaction.atomic():
            self._reverse_user_update(self)
            super().delete(*args, **kwargs)

    # -------------------------
    # Helpers for user updates
    # -------------------------
    def _apply_user_update(self):
        """Apply changes to user balance and totals."""
        if self.type == "income":
            self.user.income_total += self.amount
            self.user.balance += self.amount
        elif self.type == "expense":
            self.user.expense_total += self.amount
            self.user.balance -= self.amount
        self.user.save(update_fields=["income_total", "expense_total", "balance"])

    def _reverse_user_update(self, instance):
        """Undo changes from an existing transaction (used for updates/deletes)."""
        if instance.type == "income":
            self.user.income_total -= instance.amount
            self.user.balance -= instance.amount
        elif instance.type == "expense":
            self.user.expense_total -= instance.amount
            self.user.balance += instance.amount
        self.user.save(update_fields=["income_total", "expense_total", "balance"])
