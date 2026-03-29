from django.urls import path
from .views import (
    InitiatePaymentView,
    ConfirmPaymentView,
    PaymentDetailView,
    PaymentListView
)

urlpatterns = [
    path('', PaymentListView.as_view(), name='payment_list'),
    path('initiate/', InitiatePaymentView.as_view(), name='initiate_payment'),
    path('<int:pk>/confirm/', ConfirmPaymentView.as_view(), name='confirm_payment'),
    path('<int:pk>/', PaymentDetailView.as_view(), name='payment_detail'),
]