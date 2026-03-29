from django.urls import path
from .views import (
    ProductReviewsView,
    CreateReviewView,
    MyReviewsView,
    ReviewDetailView
)

urlpatterns = [
    # Get reviews for a specific product
    path('product/<int:product_id>/', ProductReviewsView.as_view(), name='product_reviews'),
    # Create a new review
    path('create/', CreateReviewView.as_view(), name='create_review'),
    # Get my reviews
    path('my-reviews/', MyReviewsView.as_view(), name='my_reviews'),
    # Update or delete a review
    path('<int:pk>/', ReviewDetailView.as_view(), name='review_detail'),
]