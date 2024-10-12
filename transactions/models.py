from django.db import models
from orders.models import Order

class Transaction(models.Model):
    authority = models.CharField(max_length=36)
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    code = models.SmallIntegerField()
    card_num = models.CharField(max_length=16, null=True, blank=True)
    reference_id = models.IntegerField(null=True, blank=True)
