from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from apps.products.storefront import storefront
from apps.orders.views import available_stock, create_order

admin.site.site_header = 'Rose Shop'
admin.site.site_title = 'Rose Shop Admin'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/orders/', create_order),
    path('api/stock/<slug:slug>/', available_stock),
    path('api/catalog/', storefront),
    path('api/products/', include('apps.products.urls')),
    path('api/reviews/', include('apps.reviews.urls')),
    path('api/newsletter/', include('apps.newsletter.urls')),
    path('api/site/', include('apps.site.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
