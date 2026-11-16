from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0010_product_list_indexes'),
    ]

    operations = [
        migrations.AddField(
            model_name='heroslide',
            name='image_position',
            field=models.CharField(
                choices=[
                    ('center', 'Center'),
                    ('top', 'Top'),
                    ('bottom', 'Bottom'),
                    ('left', 'Left'),
                    ('right', 'Right'),
                    ('top_left', 'Top left'),
                    ('top_right', 'Top right'),
                    ('bottom_left', 'Bottom left'),
                    ('bottom_right', 'Bottom right'),
                ],
                default='center',
                help_text='Which part of the photo stays visible in the hero box (object-position).',
                max_length=20,
            ),
        ),
    ]
