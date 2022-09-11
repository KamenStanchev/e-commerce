from django import template

from ecommerce.store.models import Order

register = template.Library()


@register.simple_tag
def total_order_items(request):
    result = 0
    if not request.user.is_authenticated:
        return result

    if not request.user.customer:
        return result

    customer = request.user.customer
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    items = order.orderitem_set.all()

    if items:
        for item in items:
            result += item.quantity
    return result
