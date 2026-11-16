from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitesettings',
            name='contact_image',
            field=models.ImageField(
                blank=True,
                help_text='Contact Us page left column (1080×1350 px portrait recommended).',
                null=True,
                upload_to='site/contact/',
            ),
        ),
        migrations.AlterField(
            model_name='sitesettings',
            name='about_image',
            field=models.ImageField(
                blank=True,
                help_text='Home About section + About Us page (1080×1350 px recommended).',
                null=True,
                upload_to='site/about/',
            ),
        ),
    ]
