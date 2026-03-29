from rest_framework import serializers
from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    order_id = serializers.IntegerField(source='order.id', read_only=True)
    customer_email = serializers.CharField(
        source='customer.email',
        read_only=True
    )

    class Meta:
        model = Payment
        fields = [
            'id', 'order_id', 'customer_email',
            'payment_method', 'payment_status',
            'amount', 'transaction_id',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'payment_status', 'transaction_id',
            'created_at', 'updated_at'
        ]


class InitiatePaymentSerializer(serializers.Serializer):
    # Why: Used when customer initiates payment for an order
    order_id = serializers.IntegerField()
    payment_method = serializers.ChoiceField(
        choices=['credit_card', 'debit_card', 'upi', 'net_banking', 'cod']
    )


class ConfirmPaymentSerializer(serializers.Serializer):
    # Why: Used to confirm/simulate payment success or failure
    payment_status = serializers.ChoiceField(
        choices=['success', 'failed']
    )