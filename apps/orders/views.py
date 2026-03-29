from rest_framework import generics, status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Order, OrderItem, OrderTracking
from .serializers import OrderSerializer, PlaceOrderSerializer
from apps.cart.cart import Cart


class IsAdminOrSeller(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and \
               request.user.role in ['admin', 'seller']


# ============================================================
# PLACE ORDER VIEW
# ============================================================
# Why: Creates order from cart items
class PlaceOrderView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = PlaceOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Get cart
        cart = Cart(request.user.id)
        cart_data = cart.get_cart()

        # Check cart is not empty
        if not cart_data:
            return Response(
                {'error': 'Cart is empty'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Calculate total
        total = cart.get_total()

        # Create order
        order = Order.objects.create(
            customer=request.user,
            total_amount=total,
            shipping_address=serializer.validated_data['shipping_address'],
            phone=serializer.validated_data['phone'],
            notes=serializer.validated_data.get('notes', '')
        )

        # Create order items from cart
        for item in cart_data.values():
            OrderItem.objects.create(
                order=order,
                product_id=item['product_id'],
                product_name=item['name'],
                product_price=item['price'],
                quantity=item['quantity'],
                total_price=float(item['price']) * item['quantity']
            )

        # Create initial tracking
        OrderTracking.objects.create(
            order=order,
            status='pending',
            message='Order placed successfully'
        )

        # Clear cart after order placed
        cart.clear_cart()


        # Send confirmation email via Celery (background task)
        from celery_app.tasks import send_order_confirmation_email, update_product_stock
        send_order_confirmation_email.delay(
            order_id=order.id,
            customer_email=request.user.email,
            total_amount=str(order.total_amount)
        )
        update_product_stock.delay(order_id=order.id)

        return Response({
            'message': 'Order placed successfully',
            'order': OrderSerializer(order).data
        }, status=status.HTTP_201_CREATED)


# ============================================================
# ORDER LIST VIEW
# ============================================================
# Why: Customer sees their own orders
class OrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Admin sees all orders, customer sees only their own
        if self.request.user.role == 'admin':
            return Order.objects.all()
        return Order.objects.filter(customer=self.request.user)


# ============================================================
# ORDER DETAIL VIEW
# ============================================================
class OrderDetailView(generics.RetrieveAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role == 'admin':
            return Order.objects.all()
        return Order.objects.filter(customer=self.request.user)


# ============================================================
# UPDATE ORDER STATUS VIEW
# ============================================================
# Why: Admin/Seller can update order status
class UpdateOrderStatusView(APIView):
    permission_classes = [IsAdminOrSeller]

    def patch(self, request, pk):
        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response(
                {'error': 'Order not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        new_status = request.data.get('status')
        valid_statuses = ['pending', 'processing', 'shipped', 'delivered', 'cancelled']

        if new_status not in valid_statuses:
            return Response(
                {'error': f'Invalid status. Choose from {valid_statuses}'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Update order status
        order.status = new_status
        order.save()

        # Add tracking entry
        messages = {
            'processing': 'Order is being processed',
            'shipped': 'Order has been shipped',
            'delivered': 'Order delivered successfully',
            'cancelled': 'Order has been cancelled'
        }

        OrderTracking.objects.create(
            order=order,
            status=new_status,
            message=messages.get(new_status, f'Status updated to {new_status}')
        )

        return Response({
            'message': f'Order status updated to {new_status}',
            'order': OrderSerializer(order).data
        })