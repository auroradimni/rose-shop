# apps/products/serializers.py

from rest_framework import serializers

from config.media_urls import media_absolute_url
from .models import Category, Product, ProductVariant, ProductImage, HeroSlide

COLOR_HEX_MAP = {
    'Black': '#1A1A1A',
    'White': '#F5F0E8',
    'Red': '#8B1A2B',
    'Burgundy': '#8B1A2B',
    'Beige': '#C8BEB4',
    'Navy': '#1E2A4A',
    'Pink': '#E8B4B8',
    'Grey': '#9E9E9E',
    'Brown': '#6B4423',
    'Green': '#2D5016',
    'Blue': '#4A6FA5',
    'Yellow': '#E8C547',
    'Orange': '#E07A3A',
    'Purple': '#6B3FA0',
}


def _absolute_url(request, file_field):
    return media_absolute_url(request, file_field)


def _pick_primary_image(images):
    if not images:
        return None
    for media in images:
        if media.is_primary:
            return media
    for media in images:
        if media.media_type == ProductImage.MEDIA_IMAGE:
            return media
    return images[0]


def _product_thumbnail_url(request, product):
    if not product:
        return None
    images = list(product.images.all())
    media = _pick_primary_image(images)
    if not media:
        return None
    if media.media_type == ProductImage.MEDIA_VIDEO:
        return _absolute_url(request, media.image) or _absolute_url(request, media.video)
    return _absolute_url(request, media.image)


class CategorySerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'image']

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image:
            return _absolute_url(request, obj.image)

        product = None
        featured = getattr(obj, 'featured_product', None)
        if featured and featured.is_active:
            product = featured
        else:
            product = (
                Product.objects.filter(category=obj, is_active=True)
                .prefetch_related('images')
                .order_by('-created_at')
                .first()
            )

        return _product_thumbnail_url(request, product)


class HeroSlideSerializer(serializers.ModelSerializer):
    mobile_image = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    image_2 = serializers.SerializerMethodField()
    image_3 = serializers.SerializerMethodField()

    class Meta:
        model = HeroSlide
        fields = [
            'id', 'mobile_image', 'image', 'image_2', 'image_3', 'desktop_photos',
            'tag', 'title', 'href', 'order',
        ]

    def get_mobile_image(self, obj):
        field = obj.mobile_image or obj.image
        return _absolute_url(self.context.get('request'), field) if field else None

    def get_image(self, obj):
        return _absolute_url(self.context.get('request'), obj.image)

    def get_image_2(self, obj):
        return _absolute_url(self.context.get('request'), obj.image_2) if obj.image_2 else None

    def get_image_3(self, obj):
        return _absolute_url(self.context.get('request'), obj.image_3) if obj.image_3 else None


class ProductImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    video = serializers.SerializerMethodField()

    class Meta:
        model = ProductImage
        fields = [
            'id', 'media_type', 'image', 'video',
            'color', 'order', 'is_primary',
        ]

    def get_image(self, obj):
        return _absolute_url(self.context.get('request'), obj.image)

    def get_video(self, obj):
        return _absolute_url(self.context.get('request'), obj.video)


class ProductVariantSerializer(serializers.ModelSerializer):
    in_stock = serializers.ReadOnlyField()
    color_hex = serializers.SerializerMethodField()

    class Meta:
        model = ProductVariant
        fields = ['id', 'color', 'color_hex', 'size', 'stock', 'in_stock']

    def get_color_hex(self, obj):
        return COLOR_HEX_MAP.get(obj.color, '#1A1A1A')


class ProductListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for catalog/carousel lists"""
    discount_percent = serializers.ReadOnlyField()
    colors_count = serializers.SerializerMethodField()
    primary_image = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    category_slug = serializers.CharField(source='category.slug', read_only=True)
    is_hot = serializers.BooleanField(source='is_bestseller', read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'price', 'original_price',
            'discount_percent', 'colors_count', 'primary_image', 'image',
            'is_new', 'is_hot', 'is_bestseller', 'is_sale', 'category_slug',
        ]

    def get_colors_count(self, obj):
        annotated = getattr(obj, '_colors_count', None)
        if annotated is not None:
            return annotated
        return len({v.color for v in obj.variants.all()})

    def _pick_primary_media(self, obj):
        return _pick_primary_image(list(obj.images.all()))

    def get_primary_image(self, obj):
        media = self._pick_primary_media(obj)
        if not media:
            return None
        request = self.context.get('request')
        if media.media_type == ProductImage.MEDIA_VIDEO:
            return _absolute_url(request, media.image) or _absolute_url(request, media.video)
        return _absolute_url(request, media.image)

    def get_image(self, obj):
        return self.get_primary_image(obj)


class ProductDetailSerializer(serializers.ModelSerializer):
    """Full serializer for product detail page"""
    discount_percent = serializers.ReadOnlyField()
    colors_count = serializers.ReadOnlyField()
    images = ProductImageSerializer(many=True, read_only=True)
    variants = ProductVariantSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    is_hot = serializers.BooleanField(source='is_bestseller', read_only=True)

    colors = serializers.SerializerMethodField()
    sizes = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'category',
            'description', 'composition', 'care',
            'price', 'original_price', 'discount_percent',
            'colors_count', 'images', 'variants',
            'colors', 'sizes',
            'is_new', 'is_hot', 'is_bestseller', 'is_sale',
            'created_at',
        ]

    def get_colors(self, obj):
        seen = set()
        colors = []
        variants = list(obj.variants.all())
        for v in variants:
            if v.color not in seen:
                seen.add(v.color)
                in_stock = any(x.color == v.color and x.stock > 0 for x in variants)
                colors.append({
                    'name': v.color,
                    'slug': v.color.lower().replace(' ', '-'),
                    'hex': COLOR_HEX_MAP.get(v.color, '#1A1A1A'),
                    'in_stock': in_stock,
                })
        return colors

    def get_sizes(self, obj):
        variants = list(obj.variants.all())
        sizes = []
        for size_code, size_label in ProductVariant.SIZES:
            size_variants = [v for v in variants if v.size == size_code]
            if size_variants:
                in_stock = any(v.stock > 0 for v in size_variants)
                sizes.append({
                    'label': size_code,
                    'in_stock': in_stock,
                })
        return sizes
