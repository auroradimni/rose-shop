from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [('products', '0017_require_category_product_line')]
    operations = [
        migrations.AddField(model_name='product', name='order', field=models.PositiveIntegerField(default=0, help_text='Lower numbers appear first in the default storefront order.')),
        migrations.AlterModelOptions(name='product', options={'ordering': ['order', '-created_at', '-pk']}),
    ]
