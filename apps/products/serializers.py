from rest_framework import serializers
from .models import Category, Product, ProductImage


# ============================================================
# CATEGORY SERIALIZER
# ============================================================
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'id', 'name', 'slug',
            'description', 'image', 'is_active'
        ]


# ============================================================
# PRODUCT IMAGE SERIALIZER
# ============================================================
class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'is_primary']


# ============================================================
# PRODUCT LIST SERIALIZER
# ============================================================
# Why: Used for listing products — shows less fields
# to keep response fast and light
class ProductListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(
        source='category.name',
        read_only=True
    )
    seller_name = serializers.CharField(
        source='seller.get_full_name',
        read_only=True
    )
    final_price = serializers.DecimalField(
        source='get_final_price',
        max_digits=10,
        decimal_places=2,
        read_only=True
    )
    discount_percentage = serializers.FloatField(
        source='get_discount_percentage',
        read_only=True
    )

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'brand',
            'category_name', 'seller_name',
            'price', 'discount_price',
            'final_price', 'discount_percentage',
            'image', 'stock', 'is_active',
            'is_featured', 'average_rating',
            'total_reviews', 'created_at'
        ]


# ============================================================
# PRODUCT DETAIL SERIALIZER
# ============================================================
# Why: Used for single product view — shows all fields
# including multiple images
class ProductDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    seller_name = serializers.CharField(
        source='seller.get_full_name',
        read_only=True
    )
    final_price = serializers.DecimalField(
        source='get_final_price',
        max_digits=10,
        decimal_places=2,
        read_only=True
    )
    discount_percentage = serializers.FloatField(
        source='get_discount_percentage',
        read_only=True
    )

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'description',
            'brand', 'category', 'seller_name',
            'price', 'discount_price',
            'final_price', 'discount_percentage',
            'stock', 'image', 'images',
            'is_active', 'is_featured',
            'average_rating', 'total_reviews',
            'created_at', 'updated_at'
        ]


# ============================================================
# PRODUCT CREATE/UPDATE SERIALIZER
# ============================================================
# Why: Used when seller creates or updates a product
class ProductWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'name', 'slug', 'description', 'brand',
            'category', 'price', 'discount_price',
            'stock', 'image', 'is_active', 'is_featured'
        ]

    def create(self, validated_data):
        # Automatically set seller to logged in user
        validated_data['seller'] = self.context['request'].user
        return super().create(validated_data)