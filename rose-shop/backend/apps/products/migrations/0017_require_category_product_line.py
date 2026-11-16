from django.db import migrations, models
import django.db.models.deletion


def require_assignments(apps, schema_editor):
    Category = apps.get_model('products', 'Category')
    missing = Category.objects.using(schema_editor.connection.alias).filter(product_line__isnull=True)
    if missing.exists():
        ProductLine = apps.get_model('products', 'ProductLine')
        line, _ = ProductLine.objects.using(schema_editor.connection.alias).get_or_create(
            slug='unassigned',
            defaults={'name': 'Për t’u klasifikuar', 'order': 999, 'is_active': False},
        )
        missing.update(product_line=line)


class Migration(migrations.Migration):
    dependencies = [('products', '0016_productline_category_product_line')]
    operations = [
        migrations.RunPython(require_assignments, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='category',
            name='product_line',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name='categories',
                help_text='Required. Choose the product line this category belongs to.',
                to='products.productline',
            ),
        ),
    ]
