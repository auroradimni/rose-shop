from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0014_heroslide_mobile_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='is_active',
            field=models.BooleanField(
                default=True,
                help_text='Uncheck to hide this category from the shop (products stay in admin).',
            ),
        ),
    ]
