from django.shortcuts import render, redirect

from ecommerce.store.models import Product, Category, Order, OrderItem


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
    return render(request, 'checkout.html', context)


def add_product_to_cart(request, pk):
    pass


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

