from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'order', 'payment_method', 'payment_status', 'amount']
    list_filter = ['payment_status', 'payment_method']
    search_fields = ['customer__email', 'transaction_id']
    readonly_fields = ['transaction_id', 'created_at', 'updated_at']