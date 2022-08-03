from __future__ import unicode_literals
from django.contrib import admin

from .models import Vehicle


class VehicleAdmin(admin.ModelAdmin):
    list_display = (
        '__str__', 'name', 'vehicle_number'
    )
    search_fields = (
        'name',
    )


admin.site.register(Vehicle, VehicleAdmin)