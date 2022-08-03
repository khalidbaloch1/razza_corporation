from django.shortcuts import render
from django.shortcuts import render
from django.views.generic import TemplateView
from django.db.models import Sum
from django.utils import timezone
from calendar import monthrange
import datetime
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth import forms as auth_forms
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.views.generic import TemplateView, RedirectView, UpdateView, ListView
from django.views.generic import FormView
from django.http import HttpResponseRedirect, HttpResponse
from django.db import transaction
from django.contrib.auth import authenticate

from dateutil.relativedelta import relativedelta
from customer.models import Customer, CustomerLedger, CustomerCredit
from sales.models import Sales
from purchase.models import Purchase


class LoginView(FormView):
    template_name = 'login.html'
    form_class = auth_forms.AuthenticationForm

    def form_valid(self, form):
        user = form.get_user()
        auth_login(self.request, user)
        return HttpResponseRedirect(reverse('common:index'))

    def form_invalid(self, form):
        return super(LoginView, self).form_invalid(form)


class LogoutView(RedirectView):

    def dispatch(self, request, *args, **kwargs):
        auth_logout(self.request)
        return super(LogoutView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(reverse('common:login'))


class IndexView(TemplateView):
    template_name = 'index.html'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('common:login'))

        return super(
            IndexView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        return context


class DailyReports(TemplateView):
    template_name = 'reports/daily.html'

    def get_context_data(self, **kwargs):
        context = super(DailyReports, self).get_context_data(**kwargs)
        data_result = []
        for day in range(90):
            data = {}
            today_date = timezone.now() - relativedelta(days=day)
            customer_ledger = CustomerLedger.objects.filter(
                date_added__year=today_date.year,
                date_added__month=today_date.month,
                date_added__day=today_date.day,
            )
            if customer_ledger.exists():
                debit = customer_ledger.aggregate(
                    Sum('debit_amount'))
                total_debit = float(
                    debit.get('debit_amount__sum') or 0
                )

            else:
                total_debit = 0

            credit_ledger = CustomerCredit.objects.filter(
                credit_date__year=today_date.year,
                credit_date__month=today_date.month,
                credit_date__day=today_date.day,
            )
            if credit_ledger.exists():
                credit = credit_ledger.aggregate(
                    Sum('credit_amount'))
                total_credit = float(
                    credit.get('credit_amount__sum') or 0
                )

            else:
                total_credit = 0

            new_customer = Customer.objects.filter(
                date__year=today_date.year,
                date__month=today_date.month,
                date__day=today_date.day,
            ).count()

            total_new_purchase = Purchase.objects.filter(
                purchase_date__year=today_date.year,
                purchase_date__month=today_date.month,
                purchase_date__day=today_date.day,
            ).count()

            new_purchase_cost = Purchase.objects.filter(
                purchase_date__year=today_date.year,
                purchase_date__month=today_date.month,
                purchase_date__day=today_date.day,
            )
            if new_purchase_cost.exists():
                cost = new_purchase_cost.aggregate(
                    Sum('total_cost'))
                total_cost = float(
                    cost.get('total_cost__sum') or 0
                )

            else:
                total_cost = 0

            new_sales = Sales.objects.filter(
                sale_date__year=today_date.year,
                sale_date__month=today_date.month,
                sale_date__day=today_date.day,
            ).count()

            new_sales_cost = Sales.objects.filter(
                sale_date__year=today_date.year,
                sale_date__month=today_date.month,
                sale_date__day=today_date.day,
            )
            if new_sales_cost.exists():
                actual_sale = new_sales_cost.aggregate(
                    Sum('actual_sale'))
                total_paid_amount = float(
                    actual_sale.get('actual_sale__sum') or 0
                )

            else:
                total_paid_amount = 0

            data.update({
                'date': today_date.date(),
                'total_debit': total_debit,
                'total_credit': total_credit,
                'new_customer': new_customer,
                'new_sales': new_sales,
                'total_new_purchase': total_new_purchase,
                'total_cost': total_cost,
                'total_paid_amount': total_paid_amount,
                'day_profit': total_paid_amount - total_cost
            })
            data_result.append(data)

        context.update({
            'results': data_result,
        })
        return context


class WeeklyRreports(TemplateView):
    template_name = 'reports/weekly.html'

    def get_context_data(self, **kwargs):
        context = super(WeeklyRreports, self).get_context_data(**kwargs)

        data_result = []
        for week in range(1, 13):
            data = {}
            sales_start_week = timezone.now() - relativedelta(weeks=week)
            sales_end_week = timezone.now() - relativedelta(
                weeks=week - 1)

            customer_ledger = CustomerLedger.objects.filter(
                date_added__gt=sales_start_week,
                date_added__lt=sales_end_week.replace(
                    hour=23, minute=59, second=59))

            if customer_ledger.exists():
                debit = customer_ledger.aggregate(
                    Sum('debit_amount'))
                total_debit = float(
                    debit.get('debit_amount__sum') or 0
                )

            else:
                total_debit = 0

            credit_ledger = CustomerCredit.objects.filter(
                credit_date__gt=sales_start_week,
                credit_date__lt=sales_end_week.replace(
                    hour=23, minute=59, second=59))

            if credit_ledger.exists():
                credit = credit_ledger.aggregate(
                    Sum('credit_amount'))
                total_credit = float(
                    credit.get('credit_amount__sum') or 0
                )

            else:
                total_credit = 0

            new_customer = Customer.objects.filter(
                date__gt=sales_start_week,
                date__lt=sales_end_week.replace(
                    hour=23, minute=59, second=59)).count()

            new_sales = Sales.objects.filter(
                sale_date__gt=sales_start_week,
                sale_date__lt=sales_end_week.replace(
                    hour=23, minute=59, second=59)).count()

            total_new_purchase = Purchase.objects.filter(
                purchase_date__gt=sales_start_week,
                purchase_date__lt=sales_end_week.replace(
                    hour=23, minute=59, second=59)).count()

            weekly_purchase_cost = Purchase.objects.filter(
                purchase_date__gt=sales_start_week,
                purchase_date__lt=sales_end_week.replace(
                    hour=23, minute=59, second=59))

            if weekly_purchase_cost.exists():
                cost = weekly_purchase_cost.aggregate(
                    Sum('total_cost'))
                weekly_total_cost = float(
                    cost.get('total_cost__sum') or 0
                )

            else:
                weekly_total_cost = 0

            weekly_sales_cost = Sales.objects.filter(
                sale_date__gt=sales_start_week,
                sale_date__lt=sales_end_week.replace(
                    hour=23, minute=59, second=59))

            if weekly_sales_cost.exists():
                actual_sale = weekly_sales_cost.aggregate(
                    Sum('actual_sale'))
                total_paid_amount = float(
                    actual_sale.get('actual_sale__sum') or 0
                )

            else:
                total_paid_amount = 0

            data.update({
                'date': sales_start_week.date(),
                'total_debit': total_debit,
                'total_credit': total_credit,
                'new_customer': new_customer,
                'new_sales': new_sales,
                'total_new_purchase': total_new_purchase,
                'weekly_total_cost': weekly_total_cost,
                'total_paid_amount': total_paid_amount,
                'weekly_profit': total_paid_amount - weekly_total_cost
            })
            data_result.append(data)

        context.update({
            'results': data_result
        })
        return context


class MonthlyReports(TemplateView):
    template_name = 'reports/monthly.html'

    def get_context_data(self, **kwargs):
        context = super(MonthlyReports, self).get_context_data(**kwargs)
        data_result = []
        last_total = 0
        for month in range(60):
            data = {}
            date_month = timezone.now() - relativedelta(months=month)
            month_range = monthrange(
                date_month.year, date_month.month
            )
            start_month = datetime.datetime(
                date_month.year, date_month.month, 1)

            end_month = datetime.datetime(
                date_month.year, date_month.month, month_range[1]
            )

            customer_ledger = CustomerLedger.objects.filter(
                date_added__gt=start_month,
                date_added__lt=end_month.replace(
                    hour=23, minute=59, second=59))

            if customer_ledger.exists():
                debit = customer_ledger.aggregate(
                    Sum('debit_amount'))
                total_debit = float(
                    debit.get('debit_amount__sum') or 0
                )

            else:
                total_debit = 0

            new_customer = Customer.objects.filter(
                date__gt=start_month,
                date__lt=end_month.replace(
                    hour=23, minute=59, second=59)).count()

            new_sales = Sales.objects.filter(
                sale_date__gt=start_month,
                sale_date__lt=end_month.replace(
                    hour=23, minute=59, second=59)).count()

            total_new_purchase = Purchase.objects.filter(
                purchase_date__gt=start_month,
                purchase_date__lt=end_month.replace(
                    hour=23, minute=59, second=59)).count()

            total_new_purchase = Purchase.objects.filter(
                purchase_date__gt=start_month,
                purchase_date__lt=end_month.replace(
                    hour=23, minute=59, second=59)).count()

            monthly_purchase_cost = Purchase.objects.filter(
                purchase_date__gt=start_month,
                purchase_date__lt=end_month.replace(
                    hour=23, minute=59, second=59))

            if monthly_purchase_cost.exists():
                cost = monthly_purchase_cost.aggregate(
                    Sum('total_cost'))
                monthly_purchase_cost = float(
                    cost.get('total_cost__sum') or 0
                )

            else:
                monthly_purchase_cost = 0

            monthly_sales_cost = Sales.objects.filter(
                sale_date__gt=start_month,
                sale_date__lt=end_month.replace(
                    hour=23, minute=59, second=59))

            if monthly_sales_cost.exists():
                paid_amount = monthly_sales_cost.aggregate(
                    Sum('paid_amount'))
                total_paid_amount = float(
                    paid_amount.get('paid_amount__sum') or 0
                )

            else:
                total_paid_amount = 0

            data.update({
                'date': start_month.strftime('%B, %Y'),
                'total_debit': total_debit,

                'new_customer': new_customer,
                'new_sales': new_sales,
                'total_new_purchase': total_new_purchase,
                'monthly_purchase_cost': monthly_purchase_cost,
                'total_paid_amount': total_paid_amount

            })

            data_result.append(data)

        context.update({
            'results': data_result
        })
        return context
