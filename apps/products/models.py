from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# ============================================================
# CATEGORY MODEL
# ============================================================
# Why: Products are organized into categories
# Example: Electronics, Mobiles, Laptops
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(
        upload_to='categories/',
        blank=True,
        null=True
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'categories'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name


# ============================================================
# PRODUCT MODEL
# ============================================================
# Why: Main product model — stores all product details
# including price, stock, seller, category
class Product(models.Model):
    # Seller who created the product
    seller = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='products'
    )

    # Category of the product
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='products'
    )

    # Basic product details
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField()
    brand = models.CharField(max_length=100, blank=True, null=True)

    # Pricing
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )

    # Stock management
    stock = models.PositiveIntegerField(default=0)

    # Product image
    image = models.ImageField(
        upload_to='products/',
        blank=True,
        null=True
    )

    # Status
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)

    # Average rating — updated when review is added
    average_rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0.00
    )
    total_reviews = models.PositiveIntegerField(default=0)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'products'
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    # Why: Returns discounted price if available
    # otherwise returns original price
    def get_final_price(self):
        if self.discount_price:
            return self.discount_price
        return self.price

    # Why: Returns discount percentage
    def get_discount_percentage(self):
        if self.discount_price:
            discount = ((self.price - self.discount_price) / self.price) * 100
            return round(discount, 2)
        return 0


# ============================================================
# PRODUCT IMAGE MODEL
# ============================================================
# Product and Category Models for NexaMart
# Why: A product can have multiple images
# Example: Front view, back view, side view
class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField(upload_to='products/gallery/')
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'product_images'
        verbose_name = 'Product Image'
        verbose_name_plural = 'Product Images'

    def __str__(self):
        return f'Image for {self.product.name}'