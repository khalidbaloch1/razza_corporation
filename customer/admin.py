from django.contrib import admin
from customer.models import Customer, CustomerLedger, CustomerCredit


class CustomerAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'mobile', 'resident', 'address', 'city', 'date'
    )


class CustomerLedgerAdmin(admin.ModelAdmin):
    list_display = (
        '__str__', 'debit_amount', 'details', 'date_added'
    )


class CustomerCreditAdmin(admin.ModelAdmin):
    list_display = (
        '__str__', 'credit_amount', 'credit_details', 'credit_date'
    )


admin.site.register(Customer, CustomerAdmin)
admin.site.register(CustomerLedger, CustomerLedgerAdmin)
admin.site.register(CustomerCredit, CustomerCreditAdmin)

