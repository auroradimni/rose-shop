from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_heroslide'),
    ]

    operations = [
        migrations.AddField(
            model_name='productimage',
            name='media_type',
            field=models.CharField(
                choices=[('image', 'Image'), ('video', 'Video')],
                default='image',
                max_length=10,
            ),
        ),
        migrations.AddField(
            model_name='productimage',
            name='video',
            field=models.FileField(blank=True, null=True, upload_to='products/videos/'),
        ),
        migrations.AlterField(
            model_name='productimage',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='products/'),
        ),
    ]
