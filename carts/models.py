from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import UniqueConstraint
from products.models import Product

User = get_user_model()


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through="CartProduct", blank=True)


class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_quantity = models.PositiveSmallIntegerField()

    class Meta:
        constraints = [
            UniqueConstraint(fields=["cart", "product"], name="unique_product")
        ]
        # TODO: See if it's good to implement a validation on app level as well
