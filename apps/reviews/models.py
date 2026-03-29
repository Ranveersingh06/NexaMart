from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.products.models import Product

User = get_user_model()

# ============================================================
# REVIEW MODEL
# ============================================================
class Review(models.Model):
    # Who wrote the review
    customer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )

    # Which product is being reviewed
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='reviews'
    )

    # Rating 1-5 stars
    rating = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ]
    )

    # Review text
    title = models.CharField(max_length=100)
    body = models.TextField()

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'reviews'
        ordering = ['-created_at']
        # Why: One customer can only review a product once
        unique_together = ['customer', 'product']

    def __str__(self):
        return f'{self.customer.email} reviewed {self.product.name} - {self.rating}★'

    # Why: Update product average rating after review is saved
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.update_product_rating()

    def update_product_rating(self):
        product = self.product
        reviews = Review.objects.filter(product=product)
        total = reviews.count()
        if total > 0:
            avg = sum(r.rating for r in reviews) / total
            product.average_rating = round(avg, 2)
            product.total_reviews = total
            product.save()