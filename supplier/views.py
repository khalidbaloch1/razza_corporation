from django.shortcuts import render
from django.views.generic import ListView, FormView, UpdateView, DeleteView, TemplateView
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.db.models import Sum
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from supplier.models import Supplier, SupplierLedger, SupplierCredit
from supplier.forms import SupplierForm, SupplierLedgerForm, SupplierCreditForm
from purchase.models import Purchase


class AddSupplier(FormView):
    form_class = SupplierForm
    template_name = 'supplier/create_supplier.html'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('common:login'))

        return super(
            AddSupplier, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(reverse('supplier:list'))

    def form_invalid(self, form):
        return super(AddSupplier, self).form_invalid(form)


class SupplierList(ListView):
    model = Supplier
    template_name = 'supplier/supplier_list.html'
    paginate_by = 100
    ordering = 'name'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('common:login'))

        return super(
            SupplierList, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = self.queryset
        if not queryset:
            queryset = Supplier.objects.all().order_by('name')

        if self.request.GET.get('customer_name'):
            queryset = queryset.filter(
                name__icontains=self.request.GET.get('customer_name'))

        if self.request.GET.get('customer_id'):
            queryset = queryset.filter(
                cnic=self.request.GET.get('customer_id').lstrip('0')
            )

        return queryset.order_by('name')


class DeleteSupplier(DeleteView):
    model = Supplier
    success_url = reverse_lazy('supplier:list')
    success_message = ''

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('common:login'))

        return super(
            DeleteSupplier, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        messages.success(request, 'Deleted Supplier SuccessFully')
        return self.post(request, *args, **kwargs)


class DebitSupplierLedgerFormView(FormView):
    template_name = 'supplier/debit.html'
    form_class = SupplierLedgerForm

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return super(
                DebitSupplierLedgerFormView, self).dispatch(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('common:login'))

    def form_valid(self, form):
        supplier_ledger = form.save()
        return HttpResponseRedirect(
            reverse('supplier:ledger_list',
                    kwargs={'pk': supplier_ledger.supplier.id}
                    )
        )

    def get_context_data(self, **kwargs):
        context = super(
            DebitSupplierLedgerFormView, self).get_context_data(**kwargs)
        context.update({
            'supplier': Supplier.objects.get(id=self.kwargs.get('pk'))
        })
        return context


class CreditSupplierLedgerFormView(DebitSupplierLedgerFormView):
    template_name = 'supplier/credit.html'
    form_class = SupplierCreditForm

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return super(
                DebitSupplierLedgerFormView, self).dispatch(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('common:login'))

    def form_valid(self, form):
        ledger_payment = form.save()
        ledger_payment.credit_date = ledger_payment.credit_date
        ledger_payment.save()
        return HttpResponseRedirect(
            reverse('supplier:ledger_list',
                    kwargs={'pk': ledger_payment.supplier.id}
                    )
        )

    def get_context_data(self, **kwargs):
        context = super(
            CreditSupplierLedgerFormView, self).get_context_data(**kwargs)
        context.update({
            'supplier': Supplier.objects.get(id=self.kwargs.get('pk'))
        })
        return context


class SupplierLedgerListView(ListView):
    model = SupplierLedger
    template_name = 'supplier/supplier_ledger_list.html'
    paginate_by = 50

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('common:login'))

        return super(
            SupplierLedgerListView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self, **kwargs):

        queryset = self.queryset

        if not queryset:
            queryset = self.model.objects.filter(
                supplier__id=self.kwargs.get('pk')).order_by('-date_added')

        if self.request.GET.get('date_added'):
            queryset = queryset.filter(
                date_added__icontains=self.request.GET.get('date_added')
            )

        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(
            SupplierLedgerListView, self).get_context_data(**kwargs)

        credit = SupplierCredit.objects.filter(
            supplier__id=self.kwargs.get('pk')
        ).order_by('-credit_date')

        if credit.exists():
            credit_payment = credit.aggregate(Sum('credit_amount'))
            credit_payment = float(credit_payment.get('credit_amount__sum'))
        else:
            credit_payment = 0

        debits = SupplierLedger.objects.filter(
            supplier__id=self.kwargs.get('pk')
        ).order_by('-date_added')

        if debits.exists():
            debit_payment = debits.aggregate(Sum('debit_amount'))
            debit_payment = float(debit_payment.get('debit_amount__sum'))
        else:
            debit_payment = 0

        from itertools import chain
        query = list(chain(credit, debits))
        query.sort(key=lambda x: x.dated)

        context.update({
            'supplier': Supplier.objects.get(
                id=self.kwargs.get('pk')),
            'debits': debits,
            'credit': credit,
            'total_payment': credit_payment,
            'debit_payment': debit_payment,
            'remaining_amount': debit_payment - credit_payment,
            'query': query

        })
        return context


def DeleteSupplierCredit(request, pk):

    SupplierCredit.objects.get(pk=pk).delete()

    messages.success(request, 'Success Full Deleted')
    return HttpResponseRedirect(reverse('supplier:list'))


class SupplierInvoicesView(TemplateView):
    template_name = 'supplier/supplier_invoice_list.html'

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return super(
                SupplierInvoicesView, self).dispatch(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('common:login'))

    def get_context_data(self, **kwargs):
        context = super(
            SupplierInvoicesView, self).get_context_data(**kwargs)
        purchase = Purchase.objects.filter(
            supplier__id=self.kwargs.get('supplier_id')
        ).order_by('purchase_date')

        start = self.kwargs.get('start')
        end = self.kwargs.get('end')
        if start and end:
            purchase = purchase.filter(
                purchase_date__range=[start, end]
            )

        if purchase.exists():
            total_ton = purchase.aggregate(Sum('total_ton'))
            total_ton = total_ton.get('total_ton__sum')

            total_cost = purchase.aggregate(Sum('cost'))
            total_cost = total_cost.get('cost__sum')

        else:
            total_ton = 0
            total_cost = 0

        credit = SupplierCredit.objects.filter(
            supplier__id=self.kwargs.get('supplier_id')
        ).order_by('-credit_date')

        if start and end:
            credit = credit.filter(
                credit_date__range=[start, end]
            )

        if credit.exists():
            credit_amount = credit.aggregate(Sum('credit_amount'))
            credit_amount = float(credit_amount.get('credit_amount__sum'))
        else:
            credit_amount = 0

        from itertools import chain
        query = list(chain(purchase, credit))
        query.sort(key=lambda x: x.dated)

        context.update({
            'purchase': purchase,
            'supplier': Supplier.objects.get(
                id=self.kwargs.get('supplier_id')),
            'start_date': start,
            'end_date': end,
            'total_cost': total_cost,
            'total_ton': total_ton,
            'credit_amount': credit_amount,
            'query': query
        })
        return context
