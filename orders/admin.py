from .models import Order
from django.contrib import admin

# Register your models here.


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass
