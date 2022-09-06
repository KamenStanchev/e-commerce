from django.shortcuts import render

from ecommerce.store.models import Product, Category


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
    context = {}
    return render(request, 'cart.html', context)


def checkout(request):
    context = {}
    return render(request, 'checkout.html', context)
