from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from apps.products.models import Product
from .cart import Cart
from rest_framework.views import APIView

import logging
logger = logging.getLogger(__name__)
# Views 
class CartView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        cart = Cart(request.user.id)
        cart_data = cart.get_cart()
        return Response({
            'items': list(cart_data.values()),
            'total': cart.get_total(),
            'item_count': cart.get_item_count()
        })

    def post(self, request):
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity', 1))

        try:
            product = Product.objects.get(
                id=product_id,
                is_active=True
            )
        except Product.DoesNotExist:
            return Response(
                {'error': 'Product not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        if product.stock < quantity:
            return Response(
                {'error': f'Only {product.stock} items available'},
                status=status.HTTP_400_BAD_REQUEST
            )

        cart = Cart(request.user.id)
        image_url = str(product.image) if product.image else None
        cart_data = cart.add_item(
            product_id=product.id,
            quantity=quantity,
            price=product.get_final_price(),
            name=product.name,
            image=image_url
        )

        return Response({
            'message': 'Item added to cart',
            'items': list(cart_data.values()),
            'total': cart.get_total(),
            'item_count': cart.get_item_count()
        }, status=status.HTTP_200_OK)

    def delete(self, request):
        cart = Cart(request.user.id)
        cart.clear_cart()
        return Response(
            {'message': 'Cart cleared successfully'},
            status=status.HTTP_200_OK
        )


class CartItemView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, product_id):
        quantity = int(request.data.get('quantity', 1))
        cart = Cart(request.user.id)
        cart_data = cart.update_quantity(product_id, quantity)
        return Response({
            'message': 'Cart updated',
            'items': list(cart_data.values()),
            'total': cart.get_total(),
            'item_count': cart.get_item_count()
        })

    def delete(self, request, product_id):
        cart = Cart(request.user.id)
        cart_data = cart.remove_item(product_id)
        return Response({
            'message': 'Item removed from cart',
            'items': list(cart_data.values()),
            'total': cart.get_total(),
            'item_count': cart.get_item_count()
        })