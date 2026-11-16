from django.db import migrations


def sync_is_sale(apps, schema_editor):
    Product = apps.get_model('products', 'Product')
    for product in Product.objects.all():
        original = product.original_price
        price = product.price
        if original is not None and original > price:
            product.is_sale = True
        else:
            product.is_sale = False
        product.save(update_fields=['is_sale'])


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0008_category_featured_product'),
    ]

    operations = [
        migrations.RunPython(sync_is_sale, migrations.RunPython.noop),
    ]
