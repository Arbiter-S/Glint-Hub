from .models import Product
from django.contrib import admin

# Register your models here.


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass
