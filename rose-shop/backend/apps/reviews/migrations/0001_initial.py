from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='CustomerReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(help_text='Instagram-style handle, e.g. finessia.fan (without @)', max_length=80)),
                ('image', models.ImageField(upload_to='reviews/')),
                ('text', models.TextField(blank=True)),
                ('order', models.PositiveIntegerField(default=0)),
                ('is_published', models.BooleanField(default=False, help_text='Show on the homepage only when checked.')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Customer review',
                'verbose_name_plural': 'Customer reviews',
                'ordering': ['order', '-created_at'],
            },
        ),
    ]
