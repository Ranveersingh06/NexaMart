from django.db import models
from django.contrib.auth import get_user_model
from apps.orders.models import Order

User = get_user_model()

# ============================================================
# PAYMENT MODEL
# ============================================================
class Payment(models.Model):

    PAYMENT_METHOD_CHOICES = (
        ('credit_card', 'Credit Card'),
        ('debit_card', 'Debit Card'),
        ('upi', 'UPI'),
        ('net_banking', 'Net Banking'),
        ('cod', 'Cash on Delivery'),
    )

    PAYMENT_STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('success', 'Success'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    )

    # Related order
    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name='payment'
    )

    # Customer
    customer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='payments'
    )

    # Payment details
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        default='upi'
    )
    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default='pending'
    )

    # Amount
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    # Transaction ID — generated after payment
    transaction_id = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        unique=True
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'payments'
        ordering = ['-created_at']

    def __str__(self):
        return f'Payment for Order #{self.order.id} - {self.payment_status}'