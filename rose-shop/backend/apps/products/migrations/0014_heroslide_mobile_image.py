from django.db import migrations, models


def copy_image_to_mobile(apps, schema_editor):
    HeroSlide = apps.get_model('products', 'HeroSlide')
    for slide in HeroSlide.objects.filter(mobile_image__isnull=True):
        if slide.image:
            slide.mobile_image = slide.image
            slide.save(update_fields=['mobile_image'])


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0013_heroslide_multi_desktop_images'),
    ]

    operations = [
        migrations.AddField(
            model_name='heroslide',
            name='mobile_image',
            field=models.ImageField(
                blank=True,
                help_text='Portrait photo for phones. Recommended 1080×1350 px (4:5).',
                null=True,
                upload_to='hero/mobile/',
                verbose_name='Mobile image',
            ),
        ),
        migrations.AlterField(
            model_name='heroslide',
            name='desktop_photos',
            field=models.PositiveSmallIntegerField(
                choices=[(1, '1 photo'), (2, '2 photos'), (3, '3 photos')],
                default=1,
                help_text='1, 2 or 3 photos side by side on desktop. Mobile uses Mobile image only.',
                verbose_name='Photos on desktop',
            ),
        ),
        migrations.AlterField(
            model_name='heroslide',
            name='image',
            field=models.ImageField(
                help_text='First desktop photo. With 1 photo: fills hero width. Recommended 1920×900 px.',
                upload_to='hero/desktop/',
                verbose_name='Desktop image 1',
            ),
        ),
        migrations.AlterField(
            model_name='heroslide',
            name='image_2',
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to='hero/desktop/',
                verbose_name='Desktop image 2',
            ),
        ),
        migrations.AlterField(
            model_name='heroslide',
            name='image_3',
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to='hero/desktop/',
                verbose_name='Desktop image 3',
            ),
        ),
        migrations.RunPython(copy_image_to_mobile, migrations.RunPython.noop),
    ]
