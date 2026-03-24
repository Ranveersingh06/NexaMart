# NexaMart

NexaMart is a production-ready e-commerce REST API built with Django and Django REST Framework. It covers the core functionality of a real e-commerce backend including authentication, product management, cart, orders, payments, and reviews.

This project was built to demonstrate backend development skills using a modern Python stack.

## Tech Stack

- Python 3.12
- Django 5.0.7
- Django REST Framework
- MySQL 8.0
- Redis
- Celery
- JWT Authentication (SimpleJWT)
- Swagger / Redoc (drf-yasg)
- Pytest
- Docker

## Features

- Role-based authentication — Admin, Seller, Customer
- Product management with categories, search, filtering and pagination
- Cart system powered by Redis
- Order placement with status tracking timeline
- Payment processing with transaction ID generation
- Product reviews restricted to verified purchases only
- Background email notifications via Celery
- Auto-generated API documentation with Swagger and Redoc
- Full test suite with Pytest

## Getting Started

Clone the repository

git clone https://github.com/yourusername/NexaMart.git
cd NexaMart

Create and activate virtual environment

python -m venv venv
venv\Scripts\activate

Install dependencies

pip install -r requirements.txt

Create a .env file in the root directory and add the following

SECRET_KEY=your-secret-key
DEBUG=True
DB_NAME=nexamart_db
DB_USER=root
DB_PASSWORD=your-mysql-password
DB_HOST=localhost
DB_PORT=3306
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

Run database migrations

python manage.py migrate

Create superuser

python manage.py createsuperuser

Start the development server

python manage.py runserver

## API Documentation

Once the server is running visit the following URLs

Swagger UI: http://127.0.0.1:8000/swagger/
Redoc: http://127.0.0.1:8000/redoc/
Admin Panel: http://127.0.0.1:8000/admin/

## API Endpoints

Authentication

POST /api/users/register/ — Register a new account
POST /api/users/login/ — Login and receive JWT tokens
POST /api/users/logout/ — Logout and blacklist token
GET /api/users/profile/ — View profile
PUT /api/users/profile/ — Update profile
POST /api/users/change-password/ — Change password

Products

GET /api/products/ — List all products
POST /api/products/ — Create a product (Seller only)
GET /api/products/?search=keyword — Search products
GET /api/products/?min_price=100&max_price=500 — Filter by price
GET /api/products/categories/ — List categories
POST /api/products/categories/ — Create category (Seller only)

Cart

GET /api/cart/ — View cart
POST /api/cart/ — Add item to cart
PUT /api/cart/product_id/ — Update item quantity
DELETE /api/cart/product_id/ — Remove item from cart
DELETE /api/cart/ — Clear entire cart

Orders

GET /api/orders/ — List orders
POST /api/orders/place/ — Place order from cart
GET /api/orders/id/ — Order detail
PATCH /api/orders/id/status/ — Update order status (Admin/Seller)

Payments

GET /api/payments/ — List payments
POST /api/payments/initiate/ — Initiate payment
POST /api/payments/id/confirm/ — Confirm payment

Reviews

GET /api/reviews/product/id/ — Get product reviews
POST /api/reviews/create/ — Write a review
GET /api/reviews/my-reviews/ — View your reviews

## Running Tests

pytest tests/ -v

## Running with Docker

docker-compose up --build

## Notes

- Cart data is stored in Redis and expires after 7 days
- Only customers with a delivered order can review that product
- JWT access tokens expire after 1 day, refresh tokens after 7 days
- Celery handles email notifications asynchronously

Initial setup completed.