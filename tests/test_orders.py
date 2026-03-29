import pytest
from rest_framework import status
from apps.products.models import Category, Product


# ============================================================
# ORDER TESTS
# ============================================================
@pytest.mark.django_db
class TestOrders:

    def setup_method(self):
        # Why: Setup test data before each test
        pass

    def test_place_order_empty_cart(self, customer_client):
        # Why: Test that order cannot be placed with empty cart
        url = '/api/orders/place/'
        data = {
            'shipping_address': '123 Test Street',
            'phone': '9876543210'
        }
        response = customer_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['error'] == 'Cart is empty'

    def test_get_orders_authenticated(self, customer_client):
        # Why: Test that authenticated customer can see their orders
        url = '/api/orders/'
        response = customer_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_get_orders_unauthenticated(self, api_client):
        # Why: Test that unauthenticated user cannot see orders
        url = '/api/orders/'
        response = api_client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_update_order_status_as_customer_fails(
        self, customer_client
    ):
        # Why: Test that customer cannot update order status
        url = '/api/orders/1/status/'
        data = {'status': 'delivered'}
        response = customer_client.patch(url, data, format='json')
        assert response.status_code == status.HTTP_403_FORBIDDEN