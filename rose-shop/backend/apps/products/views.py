# apps/products/views.py

from django.db.models import Count, F, Prefetch, Q
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as df

from .models import Category, Product, HeroSlide, ProductImage, ProductLine
from .serializers import (
    CategorySerializer,
    ProductLineSerializer,
    ProductListSerializer,
    ProductDetailSerializer,
    HeroSlideSerializer,
)


class ProductPagination(PageNumberPagination):
    page_size = 24
    page_size_query_param = 'page_size'
    max_page_size = 48


class ProductFilter(df.FilterSet):
    category = df.CharFilter(field_name='category__slug')
    product_line = df.CharFilter(field_name='category__product_line__slug')
    line = df.CharFilter(field_name='category__product_line__slug')
    min_price = df.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = df.NumberFilter(field_name='price', lookup_expr='lte')
    is_new = df.BooleanFilter()
    is_hot = df.BooleanFilter()
    is_bestseller = df.BooleanFilter()
    on_sale = df.BooleanFilter(method='filter_on_sale')
    size = df.CharFilter(method='filter_by_size')

    def filter_on_sale(self, queryset, name, value):
        if value:
            return queryset.filter(original_price__gt=F('price'))
        return queryset

    def filter_by_size(self, queryset, name, value):
        """?size=XS,M,L — products with at least one in-stock variant in those sizes."""
        if not value:
            return queryset
        sizes = [s.strip() for s in value.split(',') if s.strip()]
        if not sizes:
            return queryset
        return queryset.filter(
            variants__size__in=sizes,
            variants__stock__gt=0,
        ).distinct()

    class Meta:
        model = Product
        fields = ['category', 'product_line', 'line', 'is_new', 'is_hot', 'is_bestseller']


class ProductLineViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProductLineSerializer
    lookup_field = 'slug'
    pagination_class = None

    def get_queryset(self):
        return ProductLine.objects.filter(is_active=True)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    pagination_class = None

    def get_queryset(self):
        # Light list — only featured product thumb, not every product in each category
        qs = Category.objects.select_related('featured_product', 'product_line').prefetch_related(
            Prefetch(
                'featured_product__images',
                queryset=ProductImage.objects.filter(
                    media_type=ProductImage.MEDIA_IMAGE
                ).order_by('-is_primary', 'order'),
            ),
        ).filter(is_active=True).filter(
            Q(product_line__isnull=True) | Q(product_line__is_active=True)
        )
        line = self.request.query_params.get('line') or self.request.query_params.get('product_line')
        if line:
            qs = qs.filter(product_line__slug=line)
        return qs


def _visible_products_queryset():
    """Active products in active categories (or without category)."""
    return Product.objects.filter(is_active=True).filter(
        Q(category__isnull=True) |
        Q(category__is_active=True, category__product_line__isnull=True) |
        Q(category__is_active=True, category__product_line__is_active=True)
    )


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['name', 'description', 'category__name']
    ordering_fields = ['order', 'price', 'created_at', 'id']
    ordering = ['order', '-created_at', '-id']
    lookup_field = 'slug'
    pagination_class = ProductPagination

    def get_queryset(self):
        if self.action == 'retrieve':
            return (
                _visible_products_queryset()
                .select_related('category', 'category__product_line')
                .prefetch_related('images', 'variants')
            )

        image_qs = ProductImage.objects.order_by('-is_primary', 'order')
        return (
            _visible_products_queryset()
            .select_related('category', 'category__product_line')
            .annotate(_colors_count=Count('variants__color', distinct=True))
            .prefetch_related(Prefetch('images', queryset=image_qs))
        )

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProductDetailSerializer
        return ProductListSerializer

    @action(detail=False, methods=['get'], url_path='new-arrivals')
    def new_arrivals(self, request):
        qs = self.get_queryset().filter(is_new=True)[:12]
        serializer = ProductListSerializer(qs, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='bestsellers')
    def bestsellers(self, request):
        qs = self.get_queryset().filter(is_bestseller=True)[:12]
        serializer = ProductListSerializer(qs, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def sale(self, request):
        qs = self.get_queryset().filter(is_sale=True, original_price__gt=F('price'))[:12]
        serializer = ProductListSerializer(qs, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='sale-summary')
    def sale_summary(self, request):
        prices = self.get_queryset().filter(
            is_sale=True, original_price__gt=F('price'), price__gte=0,
        ).values_list('price', 'original_price')
        maximum = max(
            (int((original - price) * 100 / original) for price, original in prices),
            default=0,
        )
        return Response({'max_discount_percent': maximum})

    @action(detail=False, methods=['get'], url_path='active-ids')
    def active_ids(self, request):
        """IDs of active products — used to prune stale wishlist entries."""
        ids = list(
            Product.objects.filter(is_active=True).values_list('id', flat=True)
        )
        return Response({'ids': ids})

    @action(detail=False, methods=['get'], url_path='hero-slides')
    def hero_slides(self, request):
        qs = HeroSlide.objects.filter(is_active=True).only(
            'id', 'mobile_image', 'image', 'image_2', 'image_3', 'desktop_photos',
            'tag', 'title', 'href', 'order',
        )
        serializer = HeroSlideSerializer(qs, many=True, context={'request': request})
        return Response(serializer.data)
