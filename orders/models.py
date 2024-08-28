# 3rd party library imports
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.functions import NullIf

# local imports
from products.models import Product


User = get_user_model()

class Order(models.Model):
    statuses = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
        ('invalid', 'Invalid'),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=15, choices=statuses, default='pending')
    products = models.ManyToManyField(Product, through='OrderProduct')
    tracking_number = models.CharField(max_length=25, null=True, blank=True)
    #TODO: add the foreign key after address model in created
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    product_quantity = models.PositiveIntegerField()
    product_price = models.PositiveIntegerField()
