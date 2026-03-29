from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Review
from .serializers import ReviewSerializer, CreateReviewSerializer
from apps.products.models import Product


# ============================================================
# PRODUCT REVIEWS LIST VIEW
# ============================================================
# Why: Anyone can see reviews for a product
class ProductReviewsView(generics.ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        product_id = self.kwargs['product_id']
        return Review.objects.filter(
            product_id=product_id
        ).select_related('customer', 'product')


# ============================================================
# CREATE REVIEW VIEW
# ============================================================
# Why: Only authenticated customers can create reviews
class CreateReviewView(generics.CreateAPIView):
    serializer_class = CreateReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        review = serializer.save()

        return Response({
            'message': 'Review added successfully',
            'review': ReviewSerializer(review).data
        }, status=status.HTTP_201_CREATED)


# ============================================================
# MY REVIEWS VIEW
# ============================================================
# Why: Customer can see all their own reviews
class MyReviewsView(generics.ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Review.objects.filter(
            customer=self.request.user
        ).select_related('customer', 'product')


# ============================================================
# UPDATE/DELETE REVIEW VIEW
# ============================================================
# Why: Customer can update or delete their own review
class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Review.objects.filter(customer=self.request.user)