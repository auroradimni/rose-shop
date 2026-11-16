from django.db import migrations

DEFAULT_CARDS = [
    ('Holiday Season', 'white-dress.jpeg', 'fustane'),
    ('Rich Tones Only', 'black-dress.jpeg', 'bluza'),
    ('Outerwear Refresh', 'white-blazer.jpeg', 'veshje-e-jashtme'),
    ('Weekend Casual', 'pink-jumpsuit.jpeg', 'sportive'),
]


def import_cards(apps, schema_editor):
    TrendCard = apps.get_model('products', 'TrendCard')
    TrendCard.objects.using(schema_editor.connection.alias).bulk_create([
        TrendCard(title=title, default_image=f'/products/{image}',
                  href=f'/?k={category}#koleksioni', order=order)
        for order, (title, image, category) in enumerate(DEFAULT_CARDS)
    ])


class Migration(migrations.Migration):
    dependencies = [('products', '0021_trendcard')]
    operations = [migrations.RunPython(import_cards, migrations.RunPython.noop)]
