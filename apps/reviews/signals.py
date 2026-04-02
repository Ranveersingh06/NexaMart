from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Review


@receiver(post_save, sender=Review)
def review_created(sender, instance, created, **kwargs):
    if created:
        print(f'New review added for product: {instance.product.name}')