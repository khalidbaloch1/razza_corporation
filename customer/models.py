from django.db import models
from django.db.models import Sum
from django.utils import timezone


class Customer(models.Model):
        name = models.CharField(max_length=200)
        mobile = models.CharField(max_length=200, null=True, blank=True)
        resident = models.CharField(max_length=200, null=True, blank=True)
        address = models.CharField(max_length=200, null=True, blank=True)
        city = models.CharField(max_length=200, null=True, blank=True)
        ntn = models.CharField(max_length=200, null=True, blank=True)
        strn = models.CharField(max_length=200, null=True, blank=True)
        date = models.DateField(default=timezone.now, null=True, blank=True)

        def __str__(self):
            return self.name

        def ledger_balance(self):
            customer_ledgers = self.customer_ledger.all()
            if customer_ledgers.exists():
                debit_amount = customer_ledgers.aggregate(Sum('debit_amount'))
                debit_amount = float(debit_amount.get('debit_amount__sum'))
            else:
                debit_amount = 0

            return debit_amount

        def ledger_payment_balance(self):
            customer_credit_ledger = self.credit_ledger.all()
            if customer_credit_ledger.exists():
                credit_amount = customer_credit_ledger.aggregate(Sum('credit_amount'))
                credit_amount = float(credit_amount.get('credit_amount__sum'))
            else:
                credit_amount = 0

            return credit_amount

        def total_payment(self):
            invoices = self.sales_customer.all()
            if invoices.exists():
                total_payments = invoices.aggregate(Sum('paid_amount'))
                total_paid_amount = float(total_payments.get('paid_amount__sum'))
            return self.ledger_payment_balance() + total_paid_amount

        def remaining_balance(self):
            return self.ledger_balance() - self.ledger_payment_balance()


class CustomerLedger(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='customer_ledger')
    debit_amount = models.DecimalField(max_digits=65, decimal_places=2, default=0, blank=True, null=True)
    details = models.TextField(max_length=500, blank=True, null=True)
    date_added = models.DateField(default=timezone.now, blank=True, null=True)
    dated = models.DateField(default=timezone.now, blank=True, null=True)

    def __str__(self):
        return self.customer.name


class CustomerCredit(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='credit_ledger')
    credit_amount = models.DecimalField(max_digits=65, decimal_places=2, default=0, blank=True, null=True)
    credit_details = models.CharField(max_length=200, blank=True, null=True)
    credit_date = models.DateField(default=timezone.now, blank=True, null=True)
    dated = models.DateField(default=timezone.now, blank=True, null=True)

    def __str__(self):
        return self.customer.name
