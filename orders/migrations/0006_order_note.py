# Generated by Django 5.0.4 on 2024-09-06 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0005_alter_order_total_price"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="note",
            field=models.TextField(blank=True, null=True),
        ),
    ]
