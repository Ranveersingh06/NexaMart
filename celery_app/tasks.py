from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


# ============================================================
# SEND ORDER CONFIRMATION EMAIL TASK
# ============================================================
# Celery Background Tasks for Email Notifications
# Why: Sends order confirmation email in background
# so customer doesn't have to wait
@shared_task
def send_order_confirmation_email(order_id, customer_email, total_amount):
    subject = f'NexaMart — Order #{order_id} Confirmed!'
    message = f'''
    Dear Customer,

    Your order has been placed successfully!

    Order Details:
    - Order ID: #{order_id}
    - Total Amount: ₹{total_amount}
    - Status: Pending

    We will notify you when your order is shipped.

    Thank you for shopping with NexaMart!

    Best regards,
    NexaMart Team
    '''

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER or 'admin@nexamart.com',
        recipient_list=[customer_email],
        fail_silently=True
    )

    return f'Email sent to {customer_email} for order #{order_id}'


# ============================================================
# SEND PAYMENT SUCCESS EMAIL TASK
# ============================================================
@shared_task
def send_payment_success_email(order_id, customer_email, amount, transaction_id):
    subject = f'NexaMart — Payment Successful for Order #{order_id}'
    message = f'''
    Dear Customer,

    Your payment has been processed successfully!

    Payment Details:
    - Order ID: #{order_id}
    - Amount Paid: ₹{amount}
    - Transaction ID: {transaction_id}

    Thank you for shopping with NexaMart!

    Best regards,
    NexaMart Team
    '''

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER or 'admin@nexamart.com',
        recipient_list=[customer_email],
        fail_silently=True
    )

    return f'Payment email sent to {customer_email}'


# ============================================================
# UPDATE PRODUCT STOCK TASK
# ============================================================
# Why: Update product stock after order is placed
@shared_task
def update_product_stock(order_id):
    from apps.orders.models import Order
    from apps.products.models import Product

    try:
        order = Order.objects.get(id=order_id)
        for item in order.items.all():
            if item.product:
                product = item.product
                product.stock -= item.quantity
                if product.stock < 0:
                    product.stock = 0
                product.save()
        return f'Stock updated for order #{order_id}'
    except Exception as e:
        return f'Error updating stock: {str(e)}'