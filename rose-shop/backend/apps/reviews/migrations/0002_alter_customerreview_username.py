from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customerreview',
            name='username',
            field=models.CharField(
                blank=True,
                default='',
                help_text='Optional internal note (not shown on the website).',
                max_length=80,
            ),
        ),
    ]
