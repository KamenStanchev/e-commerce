from django.urls import path

from ecommerce.store.views import *

urlpatterns = [
    path('', store, name='store'),
    path('by_category/<str:pk>', product_by_category, name='product-by-category'),
    path('cart/', cart, name='cart'),
    path('checkout', checkout, name='checkout')
    ]
