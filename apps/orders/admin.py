from django.contrib import admin
from .models import Order, OrderItem, OrderTracking

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'status', 'payment_status', 'total_amount']
    list_filter = ['status', 'payment_status']
    search_fields = ['customer__email']

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product_name', 'quantity', 'total_price']

@admin.register(OrderTracking)
class OrderTrackingAdmin(admin.ModelAdmin):
    list_display = ['order', 'status', 'message', 'created_at']