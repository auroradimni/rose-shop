from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0011_heroslide_image_position'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='heroslide',
            name='image_position',
        ),
    ]
