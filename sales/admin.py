from django.contrib import admin
from .models import Sales


class SalesAdmin(admin.ModelAdmin):
    list_display = (
        'customer', 'bilty_no', 'item', 'vehicle', 'price_per_ton', 'total_ton', 'total_amount', 'deduction',
        'frieght_recieved', 'sub_total', 'balance', 'sale_date'
    )


admin.site.register(Sales, SalesAdmin)

