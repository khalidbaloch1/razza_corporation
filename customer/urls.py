from django.urls import path, re_path
from . import views
from customer.views import (
    AddCustomer, CustomerList, DeleteCustomer, CustomerInvoicesView,
    DebitCustomerLedgerFormView, CreditCustomerLedgerFormView, CustomerLedgerListView, CustomerLedgerUpdateView
)

urlpatterns = [
    path('add/', AddCustomer.as_view(), name='add'),
    path('list/', CustomerList.as_view(), name='list'),
    path('customer/delete/<int:pk>/', DeleteCustomer.as_view(), name='customer_delete'),
    re_path(r'^(?P<customer_id>\d+)/invoices/$', CustomerInvoicesView.as_view(), name='invoices'),
    path('customer/pdf/<int:pk>/', views.customer_pdf, name='customer_pdf'),
    re_path(
        r'^(?P<customer_id>\d+)/invoices/'
        r'start/(?P<start>.+)/end/(?P<end>.+)/$',
        CustomerInvoicesView.as_view(),
        name='invoices_filter'
    ),

    path('<int:pk>/ledger/debit/', DebitCustomerLedgerFormView.as_view(), name='ledger_debit'),
    path('<int:pk>/ledger/credit/', CreditCustomerLedgerFormView.as_view(), name='ledger_credit'),
    path('<int:pk>/ledger/list/', CustomerLedgerListView.as_view(), name='ledger_list'),
    path('ledger/update/<int:pk>/', CustomerLedgerUpdateView.as_view(), name='ledger_update'),
    path('delete/<int:pk>', views.DeleteCustomerCredit, name='delete'),

    ]
