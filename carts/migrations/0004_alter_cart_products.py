# Generated by Django 5.0.4 on 2024-08-23 05:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("carts", "0003_alter_cart_products_and_more"),
        ("products", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cart",
            name="products",
            field=models.ManyToManyField(
                blank=True, through="carts.CartProduct", to="products.product"
            ),
        ),
    ]
