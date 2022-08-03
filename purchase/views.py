from django.shortcuts import render
from django.utils import timezone
from django.views.generic import ListView, FormView, UpdateView, DeleteView, TemplateView
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.contrib import messages
from .models import Purchase
from .forms import PurchaseForm
from supplier.models import Supplier
from supplier.forms import SupplierLedgerForm
from product.models import ProductCategory
from vehicle.models import Vehicle


class AddPurchase(FormView):
    form_class = PurchaseForm
    template_name = 'purchase/create_purchase.html'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('common:login'))

        return super(
            AddPurchase, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        purchase_ledger = form.save()
        after_advance_payment = self.request.POST.get('after_advance_payment')
        if float(after_advance_payment):
            ledger_form_kwargs = {
                'supplier': purchase_ledger.supplier.id,
                'debit_amount': after_advance_payment,
                'details': ('Remaining Payment for Bilty No. %s' ' and Purchase %s.' % (purchase_ledger.bilty_no, purchase_ledger.id)),
                'date_added': purchase_ledger.purchase_date
            }
            supplier = SupplierLedgerForm(ledger_form_kwargs)
            supplier.save()
        return HttpResponseRedirect(reverse('purchase:list'))

    def form_invalid(self, form):
        return super(AddPurchase, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(AddPurchase, self).get_context_data(**kwargs)
        context.update({
            'item': ProductCategory.objects.all(),
            'supplier': Supplier.objects.all(),
            'vehicle': Vehicle.objects.all()
        })
        return context


class PurchaseList(ListView):
    model = Purchase
    template_name = 'purchase/list_purchase.html'
    paginate_by = 100
    ordering = '-purchase_date'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('common:login'))

        return super(
            PurchaseList, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = self.queryset
        if not queryset:
            queryset = Purchase.objects.all().order_by('-purchase_date')

        if self.request.GET.get('purchase_id'):
            queryset = queryset.filter(
                cnic=self.request.GET.get('purchase_id').lstrip('0')
            )

        return queryset.order_by('-purchase_date')


def deletePurchase(request, pk):

    Purchase.objects.get(pk=pk).delete()

    messages.success(request, 'Purchase Deleted SuccessFully')
    return HttpResponseRedirect(reverse('purchase:list'))


class PurchaseDetailTemplateView(TemplateView):
    template_name = 'purchase/detail_purchase.html'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('common:login'))

        return super(
            PurchaseDetailTemplateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PurchaseDetailTemplateView, self).get_context_data(**kwargs)
        context.update({
            'purchase': Purchase.objects.get(id=self.kwargs.get('pk')),
        })
        return context