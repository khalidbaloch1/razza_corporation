from django.db import models
from django.utils import timezone


class Vehicle(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    vehicle_number = models.CharField(max_length=200, null=True, blank=True)
    vehicle_owner_number = models.CharField(max_length=200, null=True, blank=True)
    date = models.DateField(default=timezone.now, null=True, blank=True)

    def __str__(self):
        return self.name
