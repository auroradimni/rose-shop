import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DEBUG = os.getenv('DJANGO_DEBUG', '0') == '1'
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY') or (
    'rose-shop-local-development-only' if DEBUG else os.environ['DJANGO_SECRET_KEY']
)
ORDER_API_TOKEN = os.environ['ORDER_API_TOKEN']
if not ORDER_API_TOKEN:
    raise ValueError('ORDER_API_TOKEN must be nonempty')

ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')
INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin', 'django.contrib.auth', 'django.contrib.contenttypes',
    'django.contrib.sessions', 'django.contrib.messages', 'django.contrib.staticfiles',
    'rest_framework', 'django_filters', 'colorfield',
    'apps.orders', 'apps.products', 'apps.reviews', 'apps.newsletter', 'apps.site',
]
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [BASE_DIR / 'templates'],
    'APP_DIRS': True,
    'OPTIONS': {'context_processors': [
        'django.template.context_processors.request',
        'django.contrib.auth.context_processors.auth',
        'django.contrib.messages.context_processors.messages',
        'apps.orders.context_processors.pending_orders',
    ]},
}]
ROOT_URLCONF = 'config.urls'
WSGI_APPLICATION = 'config.wsgi.application'
DATABASES = {'default': {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': os.getenv('ROSE_DB_PATH') or BASE_DIR / 'db.sqlite3',
}}
TIME_ZONE = 'Europe/Tirane'
USE_TZ = True
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG

STATICFILES_DIRS = [BASE_DIR / 'config' / 'static']

JAZZMIN_SETTINGS = {
    'site_title': 'Rose Shop Admin',
    'site_header': 'Rose Shop',
    'site_brand': 'Rose Shop',
    'welcome_sign': 'Welcome to Rose Shop',
    'copyright': 'Rose Shop',
    'order_with_respect_to': ['orders', 'products', 'products.productline', 'products.category',
                              'products.product', 'products.heroslide', 'reviews', 'newsletter', 'site', 'auth'],
    'topmenu_links': [
        {'name': 'View Store', 'url': os.getenv('FRONTEND_URL', 'http://127.0.0.1:3000'), 'new_window': True},
    ],
    'icons': {
        'orders.order': 'fas fa-shopping-bag',
        'products.productline': 'fas fa-layer-group',
        'products.category': 'fas fa-tags',
        'products.product': 'fas fa-tshirt',
        'products.heroslide': 'fas fa-images',
        'reviews.customerreview': 'fas fa-star',
        'newsletter.newslettersubscriber': 'fas fa-paper-plane',
        'site.sitesettings': 'fas fa-cog',
        'auth.user': 'fas fa-user',
        'auth.group': 'fas fa-users',
    },
    'custom_css': 'admin/css/jazzmin_custom.css',
}
JAZZMIN_UI_TWEAKS = {
    'brand_colour': 'navbar-danger',
    'accent': 'accent-danger',
    'navbar': 'navbar-dark',
    'navbar_fixed': True,
    'sidebar_fixed': True,
    'sidebar': 'sidebar-dark-danger',
    'button_classes': {
        'primary': 'btn-primary', 'secondary': 'btn-secondary',
        'info': 'btn-dark', 'warning': 'btn-warning', 'success': 'btn-success',
        'danger': 'btn-danger',
    },
}

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
PUBLIC_API_ORIGIN = os.getenv('PUBLIC_API_ORIGIN', 'http://127.0.0.1:8000').rstrip('/')

REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': ['rest_framework.throttling.ScopedRateThrottle'],
    'DEFAULT_THROTTLE_RATES': {'newsletter': '10/hour', 'reviews': '5/hour'},
}
