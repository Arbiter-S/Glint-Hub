# Generated by Django 5.0.4 on 2024-09-06 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_alter_orderproduct_product_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='address',
            field=models.TextField(default='does not matter'),
            preserve_default=False,
        ),
    ]