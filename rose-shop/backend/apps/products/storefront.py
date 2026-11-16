from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_GET

from .models import Category, HeroSlide, Product


def media_url(field):
    return settings.PUBLIC_API_ORIGIN + field.url if field else None


@require_GET
def storefront(request):
    categories = Category.objects.filter(is_active=True, product_line__is_active=True)
    products = Product.objects.filter(is_active=True, category__in=categories).select_related(
        'category',
    ).prefetch_related('variants', 'images')
    if slug := request.GET.get('slug'):
        products = products.filter(slug=slug)

    entries = []
    for product in products:
        variants = list(product.variants.all())
        images = [image for image in product.images.all() if image.image]
        image = next((image for image in images if image.is_primary), images[0] if images else None)
        entries.append({
            'slug': product.slug, 'name': product.name, 'cat': product.category.slug,
            'price': int(product.price), 'old': int(product.original_price) if product.is_sale else None,
            'desc': product.description, 'isNew': product.is_new, 'best': product.is_bestseller,
            'image': media_url(image.image) if image else None,
            'sizes': list(dict.fromkeys(variant.size for variant in variants)),
            'colors': list(dict.fromkeys(variant.color for variant in variants)),
            'available': [{'size': v.size, 'color': v.color} for v in variants if v.stock],
        })
    slide = HeroSlide.objects.filter(is_active=True).first()
    return JsonResponse({
        'products': entries,
        'categories': list(categories.values('slug', 'name')),
        'hero': {'title': slide.title, 'tag': slide.tag, 'href': slide.href,
                 'image': media_url(slide.image), 'mobileImage': media_url(slide.mobile_image),
                 'desktopImages': [media_url(field) for field in
                                   (slide.image, slide.image_2, slide.image_3)[:slide.desktop_photos]
                                   if field]} if slide else None,
    })
