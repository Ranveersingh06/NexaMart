from rest_framework import serializers
from .models import Order, OrderItem, OrderTracking


class OrderTrackingSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderTracking
        fields = ['status', 'message', 'created_at']


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = [
            'id', 'product', 'product_name',
            'product_price', 'quantity', 'total_price'
        ]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    tracking = OrderTrackingSerializer(many=True, read_only=True)
    customer_email = serializers.CharField(
        source='customer.email',
        read_only=True
    )

    class Meta:
        model = Order
        fields = [
            'id', 'customer_email', 'status',
            'payment_status', 'total_amount',
            'shipping_address', 'phone', 'notes',
            'items', 'tracking',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'status', 'payment_status',
            'total_amount', 'created_at', 'updated_at'
        ]


class PlaceOrderSerializer(serializers.Serializer):
    # Why: Used when customer places order from cart
    shipping_address = serializers.CharField()
    phone = serializers.CharField(max_length=15)
    notes = serializers.CharField(required=False, allow_blank=True)