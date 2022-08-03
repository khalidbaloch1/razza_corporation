from django.contrib import admin
from supplier.models import Supplier, SupplierLedger, SupplierCredit


class SupplierAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'mobile', 'address', 'city', 'date'
    )


class SupplierLedgerAdmin(admin.ModelAdmin):
    list_display = (
        '__str__', 'debit_amount', 'details', 'date_added'
    )


class SupplierCreditAdmin(admin.ModelAdmin):
    list_display = (
        '__str__', 'credit_amount', 'credit_details', 'credit_date'
    )


admin.site.register(Supplier, SupplierAdmin)
admin.site.register(SupplierLedger, SupplierLedgerAdmin)
admin.site.register(SupplierCredit, SupplierCreditAdmin)

