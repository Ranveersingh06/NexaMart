from django.urls import path
from .views import CartView, CartItemView

urlpatterns = [
    # Cart endpoints
    path('', CartView.as_view(), name='cart'),
    path('<int:product_id>/', CartItemView.as_view(), name='cart_item'),
]