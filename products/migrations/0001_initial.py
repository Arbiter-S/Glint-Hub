# Generated by Django 5.0.4 on 2024-08-23 04:47

import products.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Product",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=55)),
                ("description", models.TextField()),
                ("weight", models.DecimalField(decimal_places=2, max_digits=5)),
                ("color", models.CharField(max_length=25)),
                ("in_stock", models.SmallIntegerField(blank=True, null=True)),
                (
                    "category",
                    models.CharField(
                        choices=[
                            ("necklace", "Necklace"),
                            ("bracelet", "Bracelet"),
                            ("watch", "Watch"),
                            ("earring", "Earring"),
                        ],
                        max_length=10,
                    ),
                ),
                ("purity", models.SmallIntegerField()),
                (
                    "picture",
                    models.ImageField(
                        blank=True, null=True, upload_to=products.models.image_path
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
