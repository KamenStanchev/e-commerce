from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=40, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return f'for: {self.user}'


class Category(models.Model):
    name = models.CharField(max_length=20)
    description = models.TextField(max_length=200)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=20)
    price = models.FloatField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='static/images/', blank=True, null=True)
    description = models.TextField(max_length=400, null=True, blank=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=20, null=True, blank=True)

    @property
    def total_order_price(self):
        result = 0
        items = self.orderitem_set.all()
        for item in items:
            result += item.total_price
        return result

    def __str__(self):
        return f'purchaser: {self.customer} order date: {self.date_ordered}'


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    data_added = models.DateTimeField(auto_now_add=True)

    @property
    def total_price(self):
        result = self.quantity*self.product.price

        return result

    def __str__(self):
        return f'product: {self.order} order {self.order}'


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    address = models.TextField(max_length=50, null=True, blank=True)
    country = models.CharField(max_length=20, null=True, blank=True)
    city = models.CharField(max_length=20, null=True, blank=True)
    zipcode = models.CharField(max_length=20, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'customer: {self.customer} address: {self.country} {self.address}'

