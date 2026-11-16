import json
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction

from apps.orders.models import StockVariant
from apps.products.models import Category, Product, ProductVariant


class Command(BaseCommand):
    help = 'Import the original Rose Shop catalog and stock without overwriting admin changes.'

    @transaction.atomic
    def handle(self, *args, **options):
        source = (Path(settings.BASE_DIR).parent / 'lib' / 'products.js').read_text(encoding='utf-8-sig')
        parse = lambda name: json.JSONDecoder().raw_decode(source.split(f'export const {name} = ', 1)[1])[0]
        categories = {}
        for order, item in enumerate(parse('categories')):
            category, _ = Category.objects.get_or_create(slug=item['slug'], defaults={
                'name': item['name'], 'order': order,
            })
            categories[item['slug']] = category
        stock = {(v.product_slug, v.size, v.color): v.quantity for v in StockVariant.objects.all()}
        for order, item in enumerate(parse('products')):
            product, created = Product.objects.get_or_create(slug=item['slug'], defaults={
                'name': item['name'], 'category': categories[item['cat']], 'order': order,
                'description': item['desc'], 'price': item['price'], 'original_price': item.get('old'),
                'is_new': item.get('isNew', False), 'is_bestseller': item.get('best', False),
            })
            if not created:
                continue
            ProductVariant.objects.bulk_create([
                ProductVariant(product=product, size=size, color=color,
                               stock=stock.get((product.slug, size, color), 0))
                for size in item['sizes'] for color in item['colors']
            ])
        self.stdout.write(self.style.SUCCESS('Rose Shop catalog imported.'))
