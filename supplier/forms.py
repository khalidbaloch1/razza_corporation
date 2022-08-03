from django import forms
from supplier.models import Supplier, SupplierLedger, SupplierCredit


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = '__all__'


class SupplierLedgerForm(forms.ModelForm):
    class Meta:
        model = SupplierLedger
        fields = '__all__'


class SupplierCreditForm(forms.ModelForm):
    class Meta:
        model = SupplierCredit
        fields = '__all__'
