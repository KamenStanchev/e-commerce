from django import template

from ecommerce.store.models import Order

register = template.Library()


@register.simple_tag
def total_order_items(request):
    if not request.user.is_authenticated:
        return 0
    customer = request.user.customer
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    items = order.orderitem_set.all()
    result = 0
    if items:
        for item in items:
            result += item.quantity
    return result
