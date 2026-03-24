import json
import redis
from django.conf import settings

# ============================================================
# REDIS CONNECTION
# ============================================================
# Redis-powered Cart System for NexaMart
# Why: Connect to Redis to store cart data
redis_client = redis.StrictRedis(
    host='localhost',
    port=6379,
    db=0,
    decode_responses=True
)

# ============================================================
# CART CLASS
# ============================================================
class Cart:
    def __init__(self, user_id):
        # Why: Each user has their own cart key in Redis
        self.user_id = user_id
        self.cart_key = f'cart_{user_id}'

    def get_cart(self):
        # Why: Get cart data from Redis
        # If cart doesn't exist return empty dict
        cart_data = redis_client.get(self.cart_key)
        if cart_data:
            return json.loads(cart_data)
        return {}

    def save_cart(self, cart_data):
        # Why: Save cart data to Redis
        # Expires after 7 days automatically
        redis_client.setex(
            self.cart_key,
            60 * 60 * 24 * 7,  # 7 days
            json.dumps(cart_data)
        )

    def add_item(self, product_id, quantity, price, name, image=None):
        # Why: Add product to cart or update quantity
        cart_data = self.get_cart()
        product_id = str(product_id)

        if product_id in cart_data:
            # Product already in cart — update quantity
            cart_data[product_id]['quantity'] += quantity
        else:
            # New product — add to cart
            cart_data[product_id] = {
                'product_id': product_id,
                'name': name,
                'price': str(price),
                'quantity': quantity,
                'image': image or ''
            }

        self.save_cart(cart_data)
        return cart_data

    def remove_item(self, product_id):
        # Why: Remove a product from cart
        cart_data = self.get_cart()
        product_id = str(product_id)

        if product_id in cart_data:
            del cart_data[product_id]
            self.save_cart(cart_data)

        return cart_data

    def update_quantity(self, product_id, quantity):
        # Why: Update quantity of a product in cart
        cart_data = self.get_cart()
        product_id = str(product_id)

        if product_id in cart_data:
            if quantity <= 0:
                # Remove item if quantity is 0 or less
                del cart_data[product_id]
            else:
                cart_data[product_id]['quantity'] = quantity
            self.save_cart(cart_data)

        return cart_data

    def clear_cart(self):
        # Why: Clear entire cart — called after order is placed
        redis_client.delete(self.cart_key)

    def get_total(self):
        # Why: Calculate total price of all items in cart
        cart_data = self.get_cart()
        total = sum(
            float(item['price']) * item['quantity']
            for item in cart_data.values()
        )
        return round(total, 2)

    def get_item_count(self):
        # Why: Get total number of items in cart
        cart_data = self.get_cart()
        return sum(item['quantity'] for item in cart_data.values())