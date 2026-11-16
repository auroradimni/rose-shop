from django.db import models, transaction
from django.db.models import F


class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        CONFIRMED = 'confirmed', 'Confirmed'
        SHIPPED = 'shipped', 'Shipped'
        DELIVERED = 'delivered', 'Delivered'
        CANCELLED = 'cancelled', 'Cancelled'

    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=30)
    city = models.CharField(max_length=100)
    address = models.TextField()
    zone = models.CharField(max_length=10, choices=[('tirana', 'Tirana'), ('rest', 'Rest of Albania')])
    note = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    stock_reserved = models.BooleanField(default=False, editable=False)
    subtotal = models.PositiveIntegerField()
    shipping = models.PositiveIntegerField()
    discount = models.PositiveIntegerField()
    total = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.pk or self.status != self.Status.CANCELLED:
            return super().save(*args, **kwargs)
        update_fields = kwargs.get('update_fields')
        if update_fields is not None and 'status' not in update_fields:
            return super().save(*args, **kwargs)

        with transaction.atomic():
            released = Order.objects.filter(pk=self.pk, stock_reserved=True).update(stock_reserved=False)
            if released:
                from apps.products.models import ProductVariant

                for item in self.items.order_by('product_slug', 'size', 'color'):
                    variants = ProductVariant.objects.filter(pk=item.variant_id) if item.variant_id else (
                        ProductVariant.objects.filter(
                            product__slug=item.product_slug, size=item.size, color=item.color,
                        )
                    )
                    variants.update(stock=F('stock') + item.quantity)
            self.stock_reserved = False
            return super().save(*args, **kwargs)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Order #{self.pk} — {self.name}'


class OrderItem(models.Model):
    variant = models.ForeignKey('products.ProductVariant', on_delete=models.PROTECT, null=True, editable=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product_slug = models.SlugField(max_length=200)
    product_name = models.CharField(max_length=200)
    color = models.CharField(max_length=50)
    size = models.CharField(max_length=20)
    quantity = models.PositiveIntegerField()
    price = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.product_name} x{self.quantity}'

class StockVariant(models.Model):
    product_slug = models.SlugField(max_length=200)
    size = models.CharField(max_length=20)
    color = models.CharField(max_length=50)
    quantity = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['product_slug', 'size', 'color']
        constraints = [
            models.UniqueConstraint(fields=['product_slug', 'size', 'color'], name='unique_stock_variant'),
        ]

    def __str__(self):
        return f'{self.product_slug} / {self.size} / {self.color}'
