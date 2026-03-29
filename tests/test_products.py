import pytest
from rest_framework import status
from apps.products.models import Category, Product


# ============================================================
# PRODUCT TESTS
# ============================================================
@pytest.mark.django_db
class TestProducts:

    def test_create_category_as_seller(self, seller_client):
        # Why: Test that seller can create a category
        url = '/api/products/categories/'
        data = {
            'name': 'Test Category',
            'slug': 'test-category',
            'description': 'Test description'
        }
        response = seller_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['name'] == 'Test Category'

    def test_create_category_as_customer_fails(self, customer_client):
        # Why: Test that customer cannot create a category
        url = '/api/products/categories/'
        data = {
            'name': 'Test Category',
            'slug': 'test-category',
        }
        response = customer_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_get_products_list(self, api_client):
        # Why: Test that anyone can get products list
        url = '/api/products/'
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert 'results' in response.data

    def test_create_product_as_seller(self, seller_client, seller_user):
        # Why: Test that seller can create a product
        category = Category.objects.create(
            name='Electronics',
            slug='electronics'
        )
        url = '/api/products/'
        data = {
            'name': 'Test Product',
            'slug': 'test-product',
            'description': 'Test description',
            'category': category.id,
            'price': '999.00',
            'stock': 10,
            'is_active': True
        }
        response = seller_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['name'] == 'Test Product'

    def test_search_products(self, api_client, seller_user):
        # Why: Test product search functionality
        category = Category.objects.create(
            name='Electronics',
            slug='electronics-test'
        )
        Product.objects.create(
            name='Samsung Phone',
            slug='samsung-phone',
            description='A great phone',
            category=category,
            seller=seller_user,
            price=50000,
            stock=10
        )
        url = '/api/products/?search=Samsung'
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] >= 1