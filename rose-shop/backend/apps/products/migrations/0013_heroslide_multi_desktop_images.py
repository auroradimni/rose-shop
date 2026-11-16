from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0012_remove_heroslide_image_position'),
    ]

    operations = [
        migrations.AddField(
            model_name='heroslide',
            name='desktop_photos',
            field=models.PositiveSmallIntegerField(
                choices=[(1, '1 photo'), (2, '2 photos'), (3, '3 photos')],
                default=1,
                help_text='Side by side inside hero box. Mobile always shows primary image only.',
                verbose_name='Photos on desktop',
            ),
        ),
        migrations.AddField(
            model_name='heroslide',
            name='image_2',
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to='hero/',
                verbose_name='Image 2 (desktop only)',
            ),
        ),
        migrations.AddField(
            model_name='heroslide',
            name='image_3',
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to='hero/',
                verbose_name='Image 3 (desktop only)',
            ),
        ),
        migrations.AlterField(
            model_name='heroslide',
            name='image',
            field=models.ImageField(
                upload_to='hero/',
                verbose_name='Primary image (mobile + desktop #1)',
            ),
        ),
    ]
