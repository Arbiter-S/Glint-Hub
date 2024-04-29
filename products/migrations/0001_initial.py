# Generated by Django 5.0.4 on 2024-04-28 15:33

import products.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=55)),
                ('description', models.TextField()),
                ('weight', models.DecimalField(decimal_places=2, max_digits=5)),
                ('color', models.CharField(max_length=25)),
                ('in_stock', models.SmallIntegerField(null=True)),
                ('category', models.CharField(choices=[('neck', 'Necklace'), ('brace', 'Bracelet'), ('watch', 'Watch'), ('ear', 'Earring')], max_length=10)),
                ('purity', models.SmallIntegerField()),
                ('picture', models.ImageField(null=True, upload_to=products.models.image_path)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
