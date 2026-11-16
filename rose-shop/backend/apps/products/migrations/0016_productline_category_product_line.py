from django.db import migrations, models
import django.db.models.deletion


DEFAULT_PRODUCT_LINES = [
    ('Beachwear', 'beachwear', 1),
    ("Women's Occasionwear", 'womens-occasionwear', 2),
    ('Women Activewear', 'women-activewear', 3),
    ('Men Activewear', 'men-activewear', 4),
    ('Women Winterwear', 'women-winterwear', 5),
    ("Women's Loungewear", 'womens-loungewear', 6),
]


def seed_product_lines(apps, schema_editor):
    ProductLine = apps.get_model('products', 'ProductLine')
    Category = apps.get_model('products', 'Category')

    beachwear = None
    for name, slug, order in DEFAULT_PRODUCT_LINES:
        line, _ = ProductLine.objects.update_or_create(
            slug=slug,
            defaults={'name': name, 'order': order, 'is_active': True},
        )
        if slug == 'beachwear':
            beachwear = line

    if beachwear:
        Category.objects.filter(is_active=True, product_line__isnull=True).update(
            product_line=beachwear
        )


def remove_seed_product_lines(apps, schema_editor):
    ProductLine = apps.get_model('products', 'ProductLine')
    ProductLine.objects.filter(
        slug__in=[slug for _name, slug, _order in DEFAULT_PRODUCT_LINES]
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0015_category_is_active'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductLine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('order', models.IntegerField(default=0)),
                ('is_active', models.BooleanField(default=True, help_text='Uncheck to hide this product line from the storefront.')),
            ],
            options={
                'ordering': ['order', 'name'],
            },
        ),
        migrations.AddField(
            model_name='category',
            name='product_line',
            field=models.ForeignKey(
                blank=True,
                help_text='Controls under which product line this category appears.',
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='categories',
                to='products.productline',
            ),
        ),
        migrations.RunPython(seed_product_lines, remove_seed_product_lines),
    ]
