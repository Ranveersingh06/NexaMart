import uuid
from rest_framework import generics, status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from apps.orders.models import Order
from .models import Payment
from .serializers import (
    PaymentSerializer,
    InitiatePaymentSerializer,
    ConfirmPaymentSerializer
)


# ============================================================
# INITIATE PAYMENT VIEW
# ============================================================
# Why: Creates a payment record for an order
class InitiatePaymentView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = InitiatePaymentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        order_id = serializer.validated_data['order_id']
        payment_method = serializer.validated_data['payment_method']

        # Get order
        try:
            order = Order.objects.get(
                id=order_id,
                customer=request.user
            )
        except Order.DoesNotExist:
            return Response(
                {'error': 'Order not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Check if payment already exists
        if hasattr(order, 'payment'):
            return Response(
                {'error': 'Payment already initiated for this order'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create payment record
        payment = Payment.objects.create(
            order=order,
            customer=request.user,
            payment_method=payment_method,
            amount=order.total_amount,
            payment_status='pending'
        )

        return Response({
            'message': 'Payment initiated successfully',
            'payment': PaymentSerializer(payment).data
        }, status=status.HTTP_201_CREATED)


# ============================================================
# CONFIRM PAYMENT VIEW
# ============================================================
# Why: Simulates payment confirmation (success or failure)
# In production this would be a webhook from payment gateway
class ConfirmPaymentView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        serializer = ConfirmPaymentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Get payment
        try:
            payment = Payment.objects.get(
                id=pk,
                customer=request.user
            )
        except Payment.DoesNotExist:
            return Response(
                {'error': 'Payment not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        payment_status = serializer.validated_data['payment_status']

        # Update payment status
        payment.payment_status = payment_status

        if payment_status == 'success':
            # Generate transaction ID
            payment.transaction_id = str(uuid.uuid4())
            # Update order payment status
            payment.order.payment_status = 'paid'
            payment.order.save()

        payment.save()

        return Response({
            'message': f'Payment {payment_status}',
            'payment': PaymentSerializer(payment).data
        })


# ============================================================
# PAYMENT DETAIL VIEW
# ============================================================
# Why: Get payment details for an order
class PaymentDetailView(generics.RetrieveAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Payment.objects.filter(customer=self.request.user)


# ============================================================
# PAYMENT LIST VIEW
# ============================================================
# Why: Get all payments for logged in customer
class PaymentListView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role == 'admin':
            return Payment.objects.all()
        return Payment.objects.filter(customer=self.request.user)