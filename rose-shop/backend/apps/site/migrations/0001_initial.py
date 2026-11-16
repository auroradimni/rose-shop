from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='SiteSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('about_image', models.ImageField(
                    blank=True,
                    help_text='Shown on home About section and About Us page (1080×1350 px recommended).',
                    null=True,
                    upload_to='site/about/',
                )),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Site settings',
                'verbose_name_plural': 'Site settings',
            },
        ),
    ]
