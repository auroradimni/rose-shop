from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    image = models.ImageField(
        upload_to='categories/',
        blank=True,
        null=True,
        help_text='Optional cover image. If empty, uses featured product or latest product photo.',
    )
    featured_product = models.ForeignKey(
        'Product',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='featured_in_categories',
        help_text='Product photo shown on homepage. Leave empty to use the newest product in this category.',
    )
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(
        default=True,
        help_text='Uncheck to hide this category from the shop (products stay in admin).',
    )

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['order', 'name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(models.Model):
    order = models.PositiveIntegerField(default=0, help_text='Lower numbers appear first in the default storefront order.')
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        null=True, related_name='products'
    )
    description = models.TextField(blank=True)
    composition = models.CharField(max_length=200, blank=True)
    care = models.CharField(max_length=200, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    original_price = models.DecimalField(
        max_digits=10, decimal_places=2,
        null=True, blank=True,
        help_text='Original price before discount'
    )
    is_new = models.BooleanField(default=False)
    is_bestseller = models.BooleanField(default=False)
    is_sale = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', '-created_at', '-pk']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        self.sync_sale_from_prices()
        super().save(*args, **kwargs)

    def sync_sale_from_prices(self):
        """Sale + discount when original_price is set and higher than price."""
        if self.original_price is not None and self.original_price > self.price:
            self.is_sale = True
        else:
            self.is_sale = False

    @property
    def discount_percent(self):
        if self.original_price and self.original_price > self.price:
            return int((1 - self.price / self.original_price) * 100)
        return None

    @property
    def colors_count(self):
        return self.variants.values('color').distinct().count()

    def __str__(self):
        return self.name


class ProductVariant(models.Model):
    SIZES = [
        ('XS', 'XS'), ('S', 'S'), ('M', 'M'),
        ('L', 'L'), ('XL', 'XL'), ('XXL', 'XXL'),
        ('ONE_SIZE', 'One Size'),
    ]

    COLORS = [
        ('Black', 'Black'),
        ('White', 'White'),
        ('Red', 'Red'),
        ('Burgundy', 'Burgundy'),
        ('Beige', 'Beige'),
        ('Navy', 'Navy'),
        ('Pink', 'Pink'),
        ('Grey', 'Grey'),
        ('Brown', 'Brown'),
        ('Green', 'Green'),
        ('Blue', 'Blue'),
        ('Yellow', 'Yellow'),
        ('Orange', 'Orange'),
        ('Purple', 'Purple'),
    ]

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='variants'
    )
    color = models.CharField(max_length=50, choices=COLORS)
    size = models.CharField(max_length=10, choices=SIZES)
    stock = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('product', 'color', 'size')
        ordering = ['color', 'size']

    @property
    def in_stock(self):
        return self.stock > 0

    def __str__(self):
        return f'{self.product.name} — {self.color} / {self.size}'


class ProductImage(models.Model):
    MEDIA_IMAGE = 'image'
    MEDIA_VIDEO = 'video'
    MEDIA_TYPES = [
        (MEDIA_IMAGE, 'Image'),
        (MEDIA_VIDEO, 'Video'),
    ]

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='images'
    )
    color = models.CharField(
        max_length=50, blank=True,
        help_text='Leave blank if image applies to all colors'
    )
    media_type = models.CharField(
        max_length=10, choices=MEDIA_TYPES, default=MEDIA_IMAGE
    )
    image = models.ImageField(
        upload_to='products/', blank=True, null=True,
        help_text='Product photo, or poster/thumbnail for a video'
    )
    video = models.FileField(
        upload_to='products/videos/', blank=True, null=True,
        help_text='MP4/WebM video (when media type is Video)'
    )
    order = models.IntegerField(default=0)
    is_primary = models.BooleanField(default=False)

    class Meta:
        ordering = ['order']

    def __str__(self):
        kind = 'video' if self.media_type == self.MEDIA_VIDEO else 'image'
        return f'{self.product.name} — {kind} {self.order}'


class HeroSlide(models.Model):
    DESKTOP_PHOTOS_CHOICES = [(1, '1 photo'), (2, '2 photos'), (3, '3 photos')]

    mobile_image = models.ImageField(
        upload_to='hero/mobile/',
        blank=True,
        null=True,
        verbose_name='Mobile image',
        help_text='Portrait photo for phones. Recommended 1080×1350 px (4:5).',
    )
    image = models.ImageField(
        upload_to='hero/desktop/',
        verbose_name='Desktop image 1',
        help_text='First desktop photo. With 1 photo: fills hero width. Recommended 1920×900 px.',
    )
    image_2 = models.ImageField(
        upload_to='hero/desktop/',
        blank=True,
        null=True,
        verbose_name='Desktop image 2',
    )
    image_3 = models.ImageField(
        upload_to='hero/desktop/',
        blank=True,
        null=True,
        verbose_name='Desktop image 3',
    )
    desktop_photos = models.PositiveSmallIntegerField(
        choices=DESKTOP_PHOTOS_CHOICES,
        default=1,
        verbose_name='Photos on desktop',
        help_text='1, 2 or 3 photos side by side on desktop. Mobile uses Mobile image only.',
    )
    tag = models.CharField(max_length=100, blank=True)
    title = models.CharField(max_length=200)
    href = models.CharField(max_length=200, default='/products')
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title

    def clean(self):
        from django.core.exceptions import ValidationError

        if self.desktop_photos >= 2 and not self.image_2:
            raise ValidationError({'image_2': 'Required when desktop shows 2 or 3 photos.'})
        if self.desktop_photos >= 3 and not self.image_3:
            raise ValidationError({'image_3': 'Required when desktop shows 3 photos.'})
