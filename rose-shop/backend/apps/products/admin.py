from django.conf import settings
from django.contrib import admin
from django.utils.html import format_html
from django import forms
from django.urls import reverse
from .models import Category, Product, ProductVariant, ProductImage, HeroSlide, TrendCard

COLORS = ['Black', 'White', 'Red', 'Burgundy', 'Beige', 'Navy', 'Pink', 'Grey', 'Brown', 'Green', 'Blue', 'Yellow', 'Orange', 'Purple']
SIZES = ProductVariant.SIZES


class ProductAdminForm(forms.ModelForm):
    colors = forms.MultipleChoiceField(
        choices=[(c, c) for c in COLORS],
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='Colors'
    )
    sizes = forms.MultipleChoiceField(
        choices=SIZES,
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='Sizes'
    )

    class Meta:
        model = Product
        fields = '__all__'

    def clean(self):
        cleaned = super().clean()
        price = cleaned.get('price')
        original = cleaned.get('original_price')
        for field, value in [('price', price), ('original_price', original)]:
            if value is not None and (value < 0 or value != value.to_integral_value()):
                self.add_error(field, 'Enter a whole number of lek.')
        if price is not None and original is not None and original <= price:
            if original < price:
                self.add_error(
                    'original_price',
                    'Original price must be higher than price for a sale discount.',
                )
            elif original == price:
                cleaned['original_price'] = None
        return cleaned

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            variants = ProductVariant.objects.filter(product=self.instance)
            existing = set(variants.values_list('color', flat=True))
            self.fields['colors'].choices += [(color, color) for color in sorted(existing.difference(COLORS))]
            self.fields['colors'].initial = sorted(
                set(variants.values_list('color', flat=True))
            )
            self.fields['sizes'].initial = sorted(
                set(variants.values_list('size', flat=True))
            )


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 0
    fields = ['color', 'size', 'stock']
    readonly_fields = ['color', 'size']
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3
    fields = ['media_type', 'image', 'video', 'color', 'order', 'is_primary']

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == 'color':
            product_id = request.resolver_match.kwargs.get('object_id')
            if product_id:
                colors = set(ProductVariant.objects.filter(
                    product_id=product_id
                ).values_list('color', flat=True))
                kwargs['widget'] = forms.Select(choices=[('', '---------')] + [(c, c) for c in sorted(colors)])
        return super().formfield_for_dbfield(db_field, request, **kwargs)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'products_link', 'is_active', 'order', 'cover_preview']
    list_editable = ['is_active', 'order']
    list_filter = ['is_active']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']
    fields = ['name', 'slug', 'is_active', 'image', 'featured_product', 'order', 'products_link', 'add_product_link']
    readonly_fields = ['products_link', 'add_product_link']

    @admin.display(description='Products')
    def products_link(self, obj):
        if not obj.pk:
            return 'Save the category first.'
        return format_html('<a href="{}?category__id__exact={}">View products →</a>',
                           reverse('admin:products_product_changelist'), obj.pk)

    @admin.display(description='Add product')
    def add_product_link(self, obj):
        if not obj.pk:
            return 'Save the category first.'
        return format_html('<a href="{}?category={}">+ Add product to {}</a>',
                           reverse('admin:products_product_add'), obj.pk, obj.name)

    def cover_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="height:40px;border-radius:4px;" />',
                obj.image.url,
            )
        return '—'

    cover_preview.short_description = 'Cover'

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'featured_product':
            category_id = request.resolver_match.kwargs.get('object_id')
            if category_id:
                kwargs['queryset'] = Product.objects.filter(
                    category_id=category_id, is_active=True
                ).order_by('name')
            else:
                kwargs['queryset'] = Product.objects.none()
                kwargs['help_text'] = 'Save the category first, then pick a product.'
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    class Media:
        css = {'all': ('admin/css/jazzmin_custom.css',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    list_display = [
        'name', 'order', 'category', 'price', 'original_price',
        'discount_badge', 'is_new', 'is_bestseller', 'is_trending', 'is_sale', 'is_active', 'created_at'
    ]
    list_filter = ['category', 'is_new', 'is_bestseller', 'is_trending', 'is_sale', 'is_active']
    list_select_related = ['category']

    list_editable = ['order', 'is_new', 'is_bestseller', 'is_trending', 'is_active']
    readonly_fields = ['is_sale', 'discount_preview']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductVariantInline, ProductImageInline]

    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'category', 'order', 'description', 'composition', 'care'),
        }),
        ('Pricing', {
            'fields': (
                'price',
                'original_price',
                'discount_preview',
                'is_sale',
            ),
            'description': (
                'Set original price higher than price — discount % and Is sale '
                'update automatically when you save.'
            ),
        }),
        ('Flags', {
            'fields': ('is_new', 'is_bestseller', 'is_trending', 'is_active'),
        }),
        ('Colors & sizes', {
            'fields': ('colors', 'sizes'),
            'description': (
                'Pick available colors and sizes. After saving, set stock for each '
                'combination in the variants table below.'
            ),
        }),
    )

    class Media:
        css = {'all': ('admin/css/jazzmin_custom.css',)}

    def save_model(self, request, obj, form, change):
        obj.sync_sale_from_prices()
        super().save_model(request, obj, form, change)
        colors = form.cleaned_data.get('colors', [])
        sizes = form.cleaned_data.get('sizes', [])
        for color in colors:
            for size in sizes:
                ProductVariant.objects.get_or_create(
                    product=obj,
                    color=color,
                    size=size,
                    defaults={'stock': 0}
                )

    def discount_badge(self, obj):
        d = obj.discount_percent
        if d:
            return format_html(
                '<span style="background:#8B1A2B;color:white;padding:2px 8px;'
                'border-radius:10px;font-size:11px">-{}%</span>', d
            )
        return '—'
    discount_badge.short_description = 'Discount'

    def discount_preview(self, obj):
        d = obj.discount_percent
        if d is not None:
            return f'-{d}%'
        return '— (set original price above price)'
    discount_preview.short_description = 'Discount (auto)'


@admin.register(HeroSlide)
class HeroSlideAdmin(admin.ModelAdmin):
    list_display = ['title', 'desktop_photos', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    fields = [
        'mobile_image', 'image', 'image_2', 'image_3', 'desktop_photos',
        'tag', 'title', 'href', 'order', 'is_active',
    ]

    def save_model(self, request, obj, form, change):
        obj.full_clean()
        super().save_model(request, obj, form, change)

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == 'href':
            choices = [('/#koleksioni', 'All Products')]
            for cat in Category.objects.all():
                choices.append((f'/?k={cat.slug}#koleksioni', cat.name))
            kwargs['widget'] = forms.Select(choices=choices)
        return super().formfield_for_dbfield(db_field, request, **kwargs)

@admin.register(TrendCard)
class TrendCardAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    fields = ('title', 'image', 'image_preview', 'href', 'order', 'is_active')
    readonly_fields = ('image_preview',)
    search_fields = ('title',)

    @admin.display(description='Current image')
    def image_preview(self, obj):
        if not obj:
            return ''
        url = obj.image.url if obj.image else ''
        if not url and obj.default_image:
            url = f'{settings.FRONTEND_URL.rstrip("/")}{obj.default_image}'
        return format_html('<img src="{}" alt="" width="120">', url) if url else ''
