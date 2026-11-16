import json
from collections import Counter

from django.conf import settings
from django.db import transaction
from django.db.models import F
from django.http import JsonResponse
from django.utils.crypto import constant_time_compare
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST

from .models import Order, OrderItem, StockVariant


@csrf_exempt
@require_POST
def create_order(request):
    if not constant_time_compare(request.headers.get('Authorization', ''), f'Bearer {settings.ORDER_API_TOKEN}'):
        return JsonResponse({'error': 'Unauthorized'}, status=401)

    # The authenticated Next.js server validates the cart and calculates prices.
    data = json.loads(request.body)
    items = data.pop('items')
    requested = Counter()
    for item in items:
        requested[item['product_slug'], item['size'], item['color']] += item['quantity']

    try:
        with transaction.atomic():
            for (slug, size, color), quantity in sorted(requested.items()):
                updated = StockVariant.objects.filter(
                    product_slug=slug, size=size, color=color, quantity__gte=quantity,
                ).update(quantity=F('quantity') - quantity)
                if not updated:
                    raise InsufficientStock
            order = Order.objects.create(**data, stock_reserved=True)
            OrderItem.objects.bulk_create(OrderItem(order=order, **item) for item in items)
    except InsufficientStock:
        return JsonResponse({'error': 'Some items are no longer available in the requested quantity.'}, status=409)
    return JsonResponse({'ok': True, 'orderId': order.pk}, status=201)


class InsufficientStock(Exception):
    pass


@require_GET
def available_stock(request, slug):
    variants = StockVariant.objects.filter(product_slug=slug, quantity__gt=0)
    return JsonResponse({'variants': list(variants.values('size', 'color'))})
