# Generated by Django 5.0.4 on 2024-09-06 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0004_order_address"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="total_price",
            field=models.IntegerField(),
        ),
    ]
