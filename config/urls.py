from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Swagger imports
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# ============================================================
# SWAGGER CONFIGURATION
# ============================================================
schema_view = get_schema_view(
    openapi.Info(
        title="NexaMart API",
        default_version='v1',
        description="""
        NexaMart — A Modern E-Commerce REST API

        ## Features
        - JWT Authentication with role-based access
        - Products with categories, search & filters
        - Redis-powered Cart
        - Orders with tracking timeline
        - Payments with transaction ID
        - Reviews & ratings

        ## Authentication
        Use Bearer token in Authorization header:
        `Authorization: Bearer <your_access_token>`
        """,
        contact=openapi.Contact(email="admin@nexamart.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # API endpoints
    path('api/users/', include('apps.users.urls')),
    path('api/products/', include('apps.products.urls')),
    path('api/cart/', include('apps.cart.urls')),
    path('api/orders/', include('apps.orders.urls')),
    path('api/payments/', include('apps.payments.urls')),
    path('api/reviews/', include('apps.reviews.urls')),

    # Swagger & Redoc docs
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='redoc-ui'),
    path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )