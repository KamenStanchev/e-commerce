from django import template

from ecommerce.store.models import Order

register = template.Library()


@register.simple_tag
def total_order_items(request):
    result = 0
    if not request.user.is_authenticated:
        return result

    try:
        customer = request.user.customer
    except:
        return result

    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    items = order.orderitem_set.all()

    if items:
        for item in items:
            result += item.quantity
    return result
