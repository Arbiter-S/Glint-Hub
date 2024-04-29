from django.db import models
import datetime


# Create your models here.


def image_path(instance, filename):
    # MEDIA_ROOT / user_ < id > / < filename >
    name = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    return f"products/{instance.category}/{instance.name + '_' + name}.jpeg"


class Product(models.Model):
    necklace = "neck"
    bracelet = "brace"
    watch = "watch"
    ear = "ear"
    categories = {
        necklace: "Necklace",
        bracelet: "Bracelet",
        watch: "Watch",
        ear: "Earring",
    }

    name = models.CharField(max_length=55, null=False, blank=False)
    description = models.TextField()
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=False, blank=False)
    color = models.CharField(max_length=25, null=False, blank=False)
    in_stock = models.SmallIntegerField(null=True, blank=True)
    category = models.CharField(max_length=10, choices=categories)
    purity = models.SmallIntegerField(null=False, blank=False)
    picture = models.ImageField(upload_to=image_path, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
