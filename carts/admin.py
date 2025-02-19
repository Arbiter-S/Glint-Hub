from .models import Cart
from django.contrib import admin


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    pass
