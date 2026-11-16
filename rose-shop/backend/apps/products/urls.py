# apps/products/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, ProductViewSet, ProductLineViewSet

router = DefaultRouter()
router.register('product-lines', ProductLineViewSet, basename='product-line')
router.register('categories', CategoryViewSet, basename='category')
router.register('', ProductViewSet, basename='product')

urlpatterns = [
    path('', include(router.urls)),
]
