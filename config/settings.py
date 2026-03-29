import os
from pathlib import Path
from datetime import timedelta
import environ

# ============================================================
# BASE DIRECTORY
# ============================================================
# Build paths inside the project like this: BASE_DIR / 'subdir'
BASE_DIR = Path(__file__).resolve().parent.parent

# ============================================================
# ENVIRONMENT VARIABLES
# ============================================================
# Why: We use .env file to store sensitive data like passwords
# and secret keys so they are never pushed to GitHub
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# ============================================================
# SECURITY
# ============================================================
# Why: Secret key is used to sign cookies and tokens
SECRET_KEY = env('SECRET_KEY')

# Why: Debug should be True in development, False in production
DEBUG = env.bool('DEBUG', default=True)

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['*'])

# ============================================================
# INSTALLED APPS
# ============================================================
# Why: We need to register all apps so Django knows about them
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'rest_framework',           # Django REST Framework
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist', # JWT Authentication
    'corsheaders',              # CORS for frontend access
    'drf_yasg',                 # Swagger API docs
    'django_filters',           # Filter/search support
]

LOCAL_APPS = [
    'apps.users',
    'apps.products',
    'apps.cart',
    'apps.orders',
    'apps.payments',
    'apps.reviews',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# ============================================================
# MIDDLEWARE
# ============================================================
# Why: Middleware processes requests/responses globally
# CorsMiddleware must be at the top
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# ============================================================
# DATABASE — MySQL
# ============================================================
# Why: We use MySQL instead of default SQLite for
# production-grade relational database management
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': env('DB_HOST', default='localhost'),
        'PORT': env('DB_PORT', default='3306'),
        'OPTIONS': {
            'charset': 'utf8mb4',
        },
    }
}

# ============================================================
# CUSTOM USER MODEL
# ============================================================
# Why: We use a custom user model so we can add
# roles (Admin, Seller, Customer) to the user
AUTH_USER_MODEL = 'users.CustomUser'

# ============================================================
# PASSWORD VALIDATION
# ============================================================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ============================================================
# DJANGO REST FRAMEWORK
# ============================================================
# Why: We configure DRF to use JWT for all API endpoints
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 12,
}

# ============================================================
# JWT CONFIGURATION
# ============================================================
# Why: JWT tokens are used for secure stateless authentication
# Access token expires in 1 day, refresh token in 7 days
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'AUTH_HEADER_TYPES': ('Bearer',),
}

# ============================================================
# CORS CONFIGURATION
# ============================================================
# Why: CORS allows our frontend (HTML/JS) to make
# API calls to our Django backend
CORS_ALLOW_ALL_ORIGINS = True  # Allow all in development

# ============================================================
# CELERY CONFIGURATION
# ============================================================
# Why: Celery handles background tasks like sending
# emails and processing orders asynchronously
CELERY_BROKER_URL = env('CELERY_BROKER_URL', default='redis://localhost:6379/0')
CELERY_RESULT_BACKEND = env('CELERY_RESULT_BACKEND', default='redis://localhost:6379/0')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

# ============================================================
# EMAIL CONFIGURATION
# ============================================================
# Why: Used to send order confirmation and password reset emails
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = env('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = env.int('EMAIL_PORT', default=587)
EMAIL_USE_TLS = True
EMAIL_HOST_USER = env('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD', default='')

# ============================================================
# STATIC & MEDIA FILES
# ============================================================
# Why: Static files are CSS/JS, Media files are uploaded images
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# ============================================================
# INTERNATIONALIZATION
# ============================================================
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

# ============================================================
# DEFAULT PRIMARY KEY
# ============================================================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'