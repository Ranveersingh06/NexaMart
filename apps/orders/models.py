from django.db import models
from django.contrib.auth import get_user_model
from apps.products.models import Product

User = get_user_model()

# ============================================================
# ORDER MODEL
# ============================================================
class Order(models.Model):

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    )

    PAYMENT_STATUS_CHOICES = (
        ('unpaid', 'Unpaid'),
        ('paid', 'Paid'),
        ('refunded', 'Refunded'),
    )

    # Customer who placed the order
    customer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='orders'
    )

    # Order details
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default='unpaid'
    )

    # Pricing
    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00
    )

    # Delivery details
    shipping_address = models.TextField()
    phone = models.CharField(max_length=15)
    notes = models.TextField(blank=True, null=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'orders'
        ordering = ['-created_at']

    def __str__(self):
        return f'Order #{self.id} by {self.customer.email}'


# ============================================================
# ORDER ITEM MODEL
# ============================================================
# Why: Each order can have multiple products
class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True
    )
    product_name = models.CharField(max_length=200)
    product_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    class Meta:
        db_table = 'order_items'

    def __str__(self):
        return f'{self.product_name} x {self.quantity}'


# ============================================================
# ORDER TRACKING MODEL
# ============================================================
# Why: Tracks every status change with timestamp
# Shows customer exactly where their order is
class OrderTracking(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='tracking'
    )
    status = models.CharField(max_length=20)
    message = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'order_tracking'
        ordering = ['-created_at']

    def __str__(self):
        return f'Order #{self.order.id} - {self.status}'