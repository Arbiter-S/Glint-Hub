# Generated by Django 5.0.4 on 2024-10-05 00:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='card_num',
            field=models.CharField(blank=True, max_length=16, null=True),
        ),
    ]