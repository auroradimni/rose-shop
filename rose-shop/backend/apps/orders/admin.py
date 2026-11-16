from django.contrib import admin

from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ('product_name', 'product_slug', 'color', 'size', 'quantity', 'price')
    can_delete = False
    extra = 0

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone', 'city', 'total', 'status', 'created_at')
    list_filter = ('status', 'zone')
    search_fields = ('name', 'phone', 'city')
    readonly_fields = ('name', 'phone', 'city', 'address', 'zone', 'note',
                       'subtotal', 'shipping', 'discount', 'total', 'created_at')
    inlines = [OrderItemInline]

    def save_model(self, request, obj, form, change):
        obj.save(update_fields=['status'])

    def get_readonly_fields(self, request, obj=None):
        if obj and obj.status == Order.Status.CANCELLED:
            return (*self.readonly_fields, 'status')
        return self.readonly_fields

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False
