from django.urls import path

from ecommerce.store.views import *

urlpatterns = [
    path('', store, name='store'),
    path('cart/', cart, name='cart'),
    path('checkout', checkout, name='checkout')
    ]
