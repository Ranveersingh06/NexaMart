from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Category, Product, ProductImage
from .serializers import (
    CategorySerializer,
    ProductListSerializer,
    ProductDetailSerializer,
    ProductWriteSerializer,
    ProductImageSerializer
)
from .filters import ProductFilter


# ============================================================
# CUSTOM PERMISSION
# ============================================================
# Why: Only sellers and admins can create/update/delete products
# Customers can only view products
class IsSellerOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and \
               request.user.role in ['seller', 'admin']


# ============================================================
# CATEGORY VIEWSET
# ============================================================
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    permission_classes = [IsSellerOrAdmin]
    lookup_field = 'slug'


# ============================================================
# PRODUCT VIEWSET
# ============================================================
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(
        is_active=True
    ).select_related(
        'category', 'seller'
    ).prefetch_related('images')

    permission_classes = [IsSellerOrAdmin]

    # Why: Search by name, description, brand
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['name', 'description', 'brand']
    ordering_fields = ['price', 'created_at', 'average_rating']
    ordering = ['-created_at']

    # Why: Use different serializers for
    # list vs detail vs create/update
    def get_serializer_class(self):
        if self.action == 'list':
            return ProductListSerializer
        elif self.action == 'retrieve':
            return ProductDetailSerializer
        return ProductWriteSerializer

    # Why: Upload multiple images for a product
    @action(detail=True, methods=['post'])
    def upload_image(self, request, pk=None):
        product = self.get_object()
        serializer = ProductImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(product=product)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    # Why: Get only featured products
    @action(detail=False, methods=['get'])
    def featured(self, request):
        featured = Product.objects.filter(
            is_featured=True,
            is_active=True
        )
        serializer = ProductListSerializer(featured, many=True)
        return Response(serializer.data)