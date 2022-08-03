from django.contrib import admin
from .models import Purchase


class PurchaseAdmin(admin.ModelAdmin):
    list_display = (
        'supplier', 'bilty_no', 'item', 'advance_payment', 'vehicle', 'price_per_ton', 'total_expense',
        'total_ton', 'frieght', 'cost', 'total_cost', 'bilty_details', 'purchase_date'
    )


admin.site.register(Purchase, PurchaseAdmin)