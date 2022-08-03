from django.shortcuts import render
from django.views.generic import ListView, FormView, UpdateView, DeleteView, TemplateView
from django.http import HttpResponseRedirect
from django.db import transaction
from django.urls import reverse, reverse_lazy
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404

from django.contrib import messages

import os
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders

from django.db.models import Sum
from customer.models import Customer, CustomerLedger, CustomerCredit
from customer.forms import CustomerForm, CustomerLedgerForm, CustomerCreditForm
from sales.models import Sales


class AddCustomer(FormView):
    form_class = CustomerForm
    template_name = 'customer/create_customer.html'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('common:login'))

        return super(
            AddCustomer, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(reverse('customer:list'))

    def form_invalid(self, form):
        return super(AddCustomer, self).form_invalid(form)


class CustomerList(ListView):
    model = Customer
    template_name = 'customer/list_customer.html'
    paginate_by = 100
    ordering = 'name'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('common:login'))

        return super(
            CustomerList, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = self.queryset
        if not queryset:
            queryset = Customer.objects.all().order_by('name')

        if self.request.GET.get('customer_name'):
            queryset = queryset.filter(
                name__icontains=self.request.GET.get('customer_name'))

        if self.request.GET.get('customer_id'):
            queryset = queryset.filter(
                cnic=self.request.GET.get('customer_id').lstrip('0')
            )

        return queryset.order_by('name')


class DeleteCustomer(DeleteView):
    model = Customer
    success_url = reverse_lazy('customer:list')
    success_message = ''

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('common:login'))

        return super(
            DeleteCustomer, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        messages.success(request, 'Deleted Customer SuccessFully')
        return self.post(request, *args, **kwargs)


class CustomerLedgerListView(ListView):
    model = CustomerLedger
    template_name = 'customer/customer_ledger_list.html'
    paginate_by = 50

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('common:login'))

        return super(
            CustomerLedgerListView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self, **kwargs):

        queryset = self.queryset

        if not queryset:
            queryset = self.model.objects.filter(
                customer__id=self.kwargs.get('pk')).order_by('date_added')

        if self.request.GET.get('date_added'):
            queryset = queryset.filter(
                date__icontains=self.request.GET.get('date_added')
            )

        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(
            CustomerLedgerListView, self).get_context_data(**kwargs)

        payments = CustomerCredit.objects.filter(
            customer__id=self.kwargs.get('pk')
        ).order_by('-credit_date')

        if payments.exists():
            credit_payment = payments.aggregate(Sum('credit_amount'))
            credit_payment = float(credit_payment.get('credit_amount__sum'))
        else:
            credit_payment = 0

        debits = CustomerLedger.objects.filter(
            customer__id=self.kwargs.get('pk')
        ).order_by('-date_added')

        if debits.exists():
            debit_payment = debits.aggregate(Sum('debit_amount'))
            debit_payment = float(debit_payment.get('debit_amount__sum'))
        else:
            debit_payment = 0

        from itertools import chain
        query = list(chain(payments, debits))
        query.sort(key=lambda x: x.dated)

        context.update({
            'customer': Customer.objects.get(
                id=self.kwargs.get('pk')),
            'debits': debits,
            'payments': payments,
            'total_payment': credit_payment,
            'debit_payment': debit_payment,
            'remaining_amount': debit_payment - credit_payment,
            'query': query

        })
        return context


class DebitCustomerLedgerFormView(FormView):
    template_name = 'customer/debit.html'
    form_class = CustomerLedgerForm

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return super(
                DebitCustomerLedgerFormView, self).dispatch(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('common:login'))

    def form_valid(self, form):
        customer_ledger = form.save()
        return HttpResponseRedirect(
            reverse('customer:ledger_list',
                    kwargs={'pk': customer_ledger.customer.id})
        )

    def get_context_data(self, **kwargs):
        context = super(
            DebitCustomerLedgerFormView, self).get_context_data(**kwargs)
        context.update({
            'customer': Customer.objects.get(id=self.kwargs.get('pk'))
        })
        return context


class CreditCustomerLedgerFormView(DebitCustomerLedgerFormView):
    template_name = 'customer/credit.html'
    form_class = CustomerCreditForm

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return super(
                CreditCustomerLedgerFormView, self).dispatch(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('common:login'))

    def form_valid(self, form):
        ledger_payment = form.save()
        ledger_payment.credit_date = ledger_payment.credit_date
        ledger_payment.save()
        return HttpResponseRedirect(
            reverse('customer:ledger_list',
                    kwargs={'pk': ledger_payment.customer.id}
                    )
        )

    def get_context_data(self, **kwargs):
        context = super(
            CreditCustomerLedgerFormView, self).get_context_data(**kwargs)
        context.update({
            'customer': Customer.objects.get(id=self.kwargs.get('pk'))
        })
        return context


def DeleteCustomerCredit(request, pk):

    CustomerCredit.objects.get(pk=pk).delete()

    messages.success(request, 'Success Full Deleted')
    return HttpResponseRedirect(reverse('customer:list'))


class CustomerLedgerUpdateView(UpdateView):
    template_name = 'customer/customer_ledger_update.html'
    form_class = CustomerLedgerForm
    model = CustomerLedger

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return super(CustomerLedgerUpdateView, self).dispatch(
                request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('common:login'))

    def form_valid(self, form):
        customer_ledger = form.save()
        return HttpResponseRedirect(
            reverse('customer:ledger_list',
                    kwargs={'pk': customer_ledger.customer.id})
        )

    def get_context_data(self, **kwargs):
        context = super(CustomerLedgerUpdateView, self).get_context_data(**kwargs)
        context.update({
        })
        return context


class CustomerInvoicesView(TemplateView):
    template_name = 'customer/customer_invoice_list.html'

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return super(
                CustomerInvoicesView, self).dispatch(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('common:login'))

    def get_context_data(self, **kwargs):
        context = super(
            CustomerInvoicesView, self).get_context_data(**kwargs)
        sales = Sales.objects.filter(
            customer__id=self.kwargs.get('customer_id')
        ).order_by('-sale_date')

        start = self.kwargs.get('start')
        end = self.kwargs.get('end')
        if start and end:
            sales = sales.filter(
                sale_date__range=[start, end]
            )

        if sales.exists():
            total_ton = sales.aggregate(Sum('total_ton'))
            total_ton = total_ton.get('total_ton__sum')

            total_balance = sales.aggregate(Sum('balance'))
            total_balance = total_balance.get('balance__sum')

        else:
            total_ton = 0
            total_balance = 0

        credit = CustomerCredit.objects.filter(
            customer__id=self.kwargs.get('customer_id')
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
        query = list(chain(sales, credit))
        query.sort(key=lambda x: x.dated)

        context.update({
            'sales': sales,
            'customer': Customer.objects.get(
                id=self.kwargs.get('customer_id')),
            'start_date': start,
            'end_date': end,
            'total_balance': total_balance,
            'total_ton': total_ton,
            'credit_amount': credit_amount,
            'query': query
        })
        return context


def customer_pdf(request, pk):
    customer = Customer.objects.get(id=pk)
    template_path = 'customer/customer_pdf.html'
    context = {
        'customer': customer
    }
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')

    response['Content-Disposition'] = 'filename="CustomerReports.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
    # return render(request, 'staff/staff_payslip.html', context)
