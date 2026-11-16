from django.contrib import admin
from django.urls import path

from apps.orders.views import available_stock, create_order

admin.site.site_header = 'Rose Shop'
admin.site.site_title = 'Rose Shop Admin'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/orders/', create_order),
    path('api/stock/<slug:slug>/', available_stock),
]
