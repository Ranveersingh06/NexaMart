from rest_framework import serializers
from .models import Review
from apps.orders.models import Order, OrderItem


class ReviewSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(
        source='customer.get_full_name',
        read_only=True
    )
    product_name = serializers.CharField(
        source='product.name',
        read_only=True
    )

    class Meta:
        model = Review
        fields = [
            'id', 'customer_name', 'product_name',
            'rating', 'title', 'body',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class CreateReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['product', 'rating', 'title', 'body']

    # Why: Only customers who purchased the product can review it
    def validate(self, attrs):
        request = self.context['request']
        product = attrs['product']

        # Check if customer already reviewed this product
        if Review.objects.filter(
            customer=request.user,
            product=product
        ).exists():
            raise serializers.ValidationError(
                'You have already reviewed this product'
            )

        # Check if customer purchased this product
        purchased = OrderItem.objects.filter(
            order__customer=request.user,
            order__status='delivered',
            product=product
        ).exists()

        if not purchased:
            raise serializers.ValidationError(
                'You can only review products you have purchased'
            )

        return attrs

    def create(self, validated_data):
        validated_data['customer'] = self.context['request'].user
        return super().create(validated_data)