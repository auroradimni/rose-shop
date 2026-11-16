from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site', '0002_sitesettings_contact_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitesettings',
            name='phone',
            field=models.CharField(
                blank=True,
                help_text='Shop phone, e.g. +355 69 704 2889. Shown in footer and Contact page.',
                max_length=40,
            ),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='instagram',
            field=models.CharField(
                blank=True,
                default='finessia.al',
                help_text='Instagram username only (no @), e.g. finessia.al',
                max_length=80,
            ),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='tiktok',
            field=models.CharField(
                blank=True,
                default='finessia.al',
                help_text='TikTok username only (no @), e.g. finessia.al',
                max_length=80,
            ),
        ),
    ]
