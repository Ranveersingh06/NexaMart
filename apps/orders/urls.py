from django.urls import path
from .views import (
    PlaceOrderView,
    OrderListView,
    OrderDetailView,
    UpdateOrderStatusView
)

urlpatterns = [
    path('', OrderListView.as_view(), name='order_list'),
    path('place/', PlaceOrderView.as_view(), name='place_order'),
    path('<int:pk>/', OrderDetailView.as_view(), name='order_detail'),
    path('<int:pk>/status/', UpdateOrderStatusView.as_view(), name='update_order_status'),
]