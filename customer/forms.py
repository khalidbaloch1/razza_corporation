from django import forms
from customer.models import Customer, CustomerLedger, CustomerCredit


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'


class CustomerLedgerForm(forms.ModelForm):
    class Meta:
        model = CustomerLedger
        fields = '__all__'


class CustomerCreditForm(forms.ModelForm):
    class Meta:
        model = CustomerCredit
        fields = '__all__'
