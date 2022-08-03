from django.db import models
from django.utils import timezone


class ProductCategory(models.Model):
    product = models.CharField(max_length=200, null=True, blank=True)
    product_place = models.CharField(max_length=200, null=True, blank=True)
    date = models.DateField(default=timezone.now, null=True, blank=True)

    def __str__(self):
        return self.product
