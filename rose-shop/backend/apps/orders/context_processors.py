from django.urls import reverse

from .models import Order


def pending_orders(request):
    user = request.user
    if not request.path.startswith('/admin/') or not user.has_perm('orders.view_order'):
        return {}
    count = Order.objects.filter(status=Order.Status.PENDING).count()
    return {'admin_unread_counts': [{'url': reverse('admin:orders_order_changelist'), 'count': count}]} if count else {}
