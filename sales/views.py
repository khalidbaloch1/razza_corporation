from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.generic import ListView, FormView, UpdateView, DeleteView, TemplateView
from django.http import HttpResponseRedirect, HttpResponse
from django.db import transaction
from django.urls import reverse, reverse_lazy
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.contrib import messages

import os
from django.conf import settings
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders

from .models import Sales
from .forms import SalesForm
from customer.models import Customer
from customer.forms import CustomerLedgerForm
from product.models import ProductCategory
from vehicle.models import Vehicle


class AddSales(FormView):
    form_class = SalesForm
    template_name = 'sales/create_sales.html'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('common:login'))

        return super(
            AddSales, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        sales_invoice = form.save()
        remaining_payment = self.request.POST.get('remaining_payment')
        if float(remaining_payment):
            ledger_form_kwargs = {
                'customer': sales_invoice.customer.id,
                'debit_amount': remaining_payment,
                'details': ('Remaining Payment for Bilty No. %s' ' and Sales %s.' % (sales_invoice.bilty_no, sales_invoice.id)),
                'date_added': sales_invoice.sale_date

            }
            customer = CustomerLedgerForm(ledger_form_kwargs)
            customer.save()
        return HttpResponseRedirect(reverse('sales:list'))

    def form_invalid(self, form):
        return super(AddSales, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(AddSales, self).get_context_data(**kwargs)
        context.update({
            'item': ProductCategory.objects.all(),
            'customer': Customer.objects.all(),
            'vehicle': Vehicle.objects.all()
        })
        return context


class SalesList(ListView):
    model = Sales
    template_name = 'sales/list_sales.html'
    paginate_by = 100
    ordering = 'id'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('common:login'))

        return super(
            SalesList, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = self.queryset
        if not queryset:
            queryset = Sales.objects.all().order_by('id')

        if self.request.GET.get('sales_id'):
            queryset = queryset.filter(
                cnic=self.request.GET.get('sales_id').lstrip('0')
            )

        return queryset.order_by('id')


class SalesDetailTemplateView(TemplateView):
    template_name = 'sales/detail_sales.html'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('common:login'))

        return super(
            SalesDetailTemplateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(SalesDetailTemplateView, self).get_context_data(**kwargs)
        context.update({
            'sales': Sales.objects.get(id=self.kwargs.get('pk')),
        })
        return context


class SalesUpdateView(UpdateView):
    template_name = 'sales/sale_update.html'
    form_class = SalesForm
    model = Sales

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return super(SalesUpdateView, self).dispatch(
                request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('common:login'))

    def form_valid(self, form):
            sales_invoice = form.save(commit=False)
            remaining_payment = self.request.POST.get('remaining_payment')
            if float(remaining_payment):
                ledger_form_kwargs = {
                    'customer': sales_invoice.customer.id,
                    'debit_amount': remaining_payment,
                    'details': ('Remaining Payment for Bilty No. %s' ' and Sales %s.' % (sales_invoice.bilty_no, sales_invoice.id)),
                    'date_added': sales_invoice.sale_date

                }
                customer = CustomerLedgerForm(ledger_form_kwargs)
                customer.save()
            return HttpResponseRedirect(reverse('sales:list'))

    def get_context_data(self, **kwargs):
        context = super(SalesUpdateView, self).get_context_data(**kwargs)

        context.update({
            'item': ProductCategory.objects.all(),
            'customer': Customer.objects.all(),
            'vehicle': Vehicle.objects.all()
        })
        return context


def deleteSales(request, pk):

    Sales.objects.get(pk=pk).delete()

    messages.success(request, 'Success Full Deleted')
    return HttpResponseRedirect(reverse('sales:list'))


def sales_payslip(request, pk):

    sales = Sales.objects.get(id=pk)
    template_path = 'sales/sales_pdf.html'
    context = {
        'sales': sales
    }
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')

    response['Content-Disposition'] = 'filename="payslip.pdf"'
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
