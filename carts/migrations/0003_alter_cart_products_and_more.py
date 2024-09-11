# Generated by Django 5.0.4 on 2024-08-23 05:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0002_initial'),
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='products',
            field=models.ManyToManyField(through='carts.CartProduct', to='products.product'),
        ),
        migrations.AlterUniqueTogether(
            name='cartproduct',
            unique_together={('cart', 'product')},
        ),
    ]