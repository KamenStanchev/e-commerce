from decouple import config
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.views.generic.detail import DetailView

from ecommerce.store.forms import CustomerForm, ShippingAddressForm
from ecommerce.store.models import Product, Category, Order, OrderItem, ShippingAddress


class ProductDetail(DetailView):
    model = Product
    template_name = 'product_detail.html'
    context_object_name = 'product'


def store(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    categories_dic = {}
    for category in categories:
        category_products = Product.objects.filter(category=category)
        if category_products:
            categories_dic[category] = category_products
    context = {
        'products': products,
        'categories_dic': categories_dic,
    }
    return render(request, 'store.html', context)


def product_by_category(request, pk):
    products = Product.objects.filter(category__pk=pk)
    categories = Category.objects.all()
    categories_dic = {}
    for category in categories:
        category_products = Product.objects.filter(category=category)
        if category_products:
            categories_dic[category] = category_products
    context = {
        'products': products,
        'categories_dic': categories_dic,
    }
    print(products[0].image)
    return render(request, 'store.html', context)


def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        order = None
        items = []
    context = {
        'items': items,
        'order': order,
    }
    return render(request, 'cart.html', context)


def checkout(request):
    customer = request.user.customer
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    items = order.orderitem_set.all()
    shipping_address, created = ShippingAddress.objects.get_or_create(customer=customer, order=order)

    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        form1 = ShippingAddressForm(request.POST, instance=shipping_address)
        if form.is_valid() and form1.is_valid():
            form.save()
            form1.save()

            customer_name = form.cleaned_data['name']
            customer_email = form.cleaned_data['email']

            customer_address = form1.cleaned_data['address']
            customer_city = form1.cleaned_data['city']
            customer_zipcode = form1.cleaned_data['zipcode']
            customer_country = form1.cleaned_data['country']

            html_to_customer = render_to_string('emails/email_to_customer.html', {
                'customer_name': customer_name,
                'shipping_address': f"{customer_country}, {customer_zipcode}, {customer_city}, {customer_address}",
                'items': items, 'order': order
            })

            send_mail(f'{customer_name}', 'Text to message', 'kamen.stanchev.work@gmail.com',
                      [customer_email], html_message=html_to_customer)

            send_mail(f'New purchase from: {customer_name}', 'Text to message', 'kamen.stanchev.work@gmail.com',
                      ['kamenstanchev81@gmail.com'], html_message=html_to_customer)

            order.complete = True
            order.save()

            return redirect('store')

    form = CustomerForm(instance=customer)
    form1 = ShippingAddressForm(instance=shipping_address)
    context = {
        'items': items,
        'order': order,
        'form': form,
        'form1': form1,
        'customer': customer,
    }

    return render(request, 'checkout.html', context)


def add_product_to_cart(request, pk):
    if not request.user.is_authenticated:
        return redirect('login')
    customer = request.user.customer
    product = Product.objects.get(id=pk)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    items = order.orderitem_set.all()
    product_in_ordered_items = order.orderitem_set.filter(order__orderitem__product=product)

    # if product is already in cart -> increase its quantity and safe
    if product_in_ordered_items:
        for item in items:
            if item.product.id == product.id:
                item.quantity += 1
                item.save()
                return redirect(request.META.get('HTTP_REFERER', 'store'))

    # if product not in cart -> create new OrderItem with foreign key current product and safe.
    new_order_item = OrderItem.objects.create(product=product, order=order, quantity=1)
    new_order_item.save()
    return redirect(request.META.get('HTTP_REFERER', 'store'))


def increase_quantity_of_ordered_item(request, pk):
    ordered_item = OrderItem.objects.get(id=pk)
    ordered_item.quantity += 1
    ordered_item.save()
    return redirect('cart')


def decrease_quantity_of_ordered_item(request, pk):
    ordered_item = OrderItem.objects.get(id=pk)
    ordered_item.quantity -= 1
    ordered_item.save()
    if ordered_item.quantity == 0:
        ordered_item.delete()
    return redirect('cart')
