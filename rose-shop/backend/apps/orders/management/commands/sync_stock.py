import json
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction

from apps.orders.models import StockVariant


class Command(BaseCommand):
    help = 'Create zero-stock variants for new entries in the Rose Shop catalog.'

    @transaction.atomic
    def handle(self, *args, **options):
        catalog = (Path(settings.BASE_DIR).parent / 'lib' / 'products.js').read_text(encoding='utf-8-sig')
        entries = catalog.split('export const products = ', 1)[1]
        products, _ = json.JSONDecoder().raw_decode(entries.lstrip())
        created = 0
        for product in products:
            for size in product['sizes']:
                for color in product['colors']:
                    _, added = StockVariant.objects.get_or_create(
                        product_slug=product['slug'], size=size, color=color,
                    )
                    created += added
        self.stdout.write(f'Created {created} stock variants.')
