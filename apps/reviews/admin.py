from django.contrib import admin
from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['customer', 'product', 'rating', 'title', 'created_at']
    list_filter = ['rating']
    search_fields = ['customer__email', 'product__name']
    readonly_fields = ['created_at', 'updated_at']