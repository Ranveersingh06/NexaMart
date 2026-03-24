import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()


# ============================================================
# WHY: conftest.py provides reusable fixtures for all tests
# Fixtures are like setup functions that run before each test
# Pytest Configuration and Fixtures for NexaMart
# ============================================================

@pytest.fixture
def api_client():
    # Why: Creates a test API client to make requests
    return APIClient()


@pytest.fixture
def create_user():
    # Why: Creates a test user with given role
    def make_user(email, password, role='customer'):
        user = User.objects.create_user(
            email=email,
            password=password,
            first_name='Test',
            last_name='User',
            role=role
        )
        return user
    return make_user


@pytest.fixture
def customer_user(create_user):
    # Why: Creates a customer user for testing
    return create_user(
        email='testcustomer@nexamart.com',
        password='Test@1234',
        role='customer'
    )


@pytest.fixture
def seller_user(create_user):
    # Why: Creates a seller user for testing
    return create_user(
        email='testseller@nexamart.com',
        password='Test@1234',
        role='seller'
    )


@pytest.fixture
def admin_user(create_user):
    # Why: Creates an admin user for testing
    return create_user(
        email='testadmin@nexamart.com',
        password='Test@1234',
        role='admin'
    )


@pytest.fixture
def customer_client(api_client, customer_user):
    # Why: Creates an authenticated client for customer
    api_client.force_authenticate(user=customer_user)
    return api_client


@pytest.fixture
def seller_client(api_client, seller_user):
    # Why: Creates an authenticated client for seller
    api_client.force_authenticate(user=seller_user)
    return api_client


@pytest.fixture
def admin_client(api_client, admin_user):
    # Why: Creates an authenticated client for admin
    api_client.force_authenticate(user=admin_user)
    return api_client