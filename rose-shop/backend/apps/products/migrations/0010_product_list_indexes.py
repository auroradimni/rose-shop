from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0009_sync_product_is_sale'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['is_active', '-created_at'], name='prod_active_created_idx'),
        ),
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['is_active', 'category'], name='prod_active_cat_idx'),
        ),
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['is_active', 'is_new'], name='prod_active_new_idx'),
        ),
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['is_active', 'is_bestseller'], name='prod_active_best_idx'),
        ),
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['is_active', 'price'], name='prod_active_price_idx'),
        ),
    ]
