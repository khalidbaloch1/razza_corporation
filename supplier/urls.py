from django.urls import path, re_path
from . import views
from supplier.views import (
    AddSupplier, SupplierList, DeleteSupplier, SupplierInvoicesView,
    DebitSupplierLedgerFormView, CreditSupplierLedgerFormView, SupplierLedgerListView
)

urlpatterns = [
    path('add/', AddSupplier.as_view(), name='add'),
    path('list/', SupplierList.as_view(), name='list'),
    path('delete//<int:pk>/', DeleteSupplier.as_view(), name='delete'),
    re_path(
        r'^(?P<supplier_id>\d+)/invoices/$',
        SupplierInvoicesView.as_view(),
        name='invoices'
    ),

    re_path(
        r'^(?P<supplier_id>\d+)/invoices/'
        r'start/(?P<start>.+)/end/(?P<end>.+)/$',
        SupplierInvoicesView.as_view(),
        name='invoices_filter'
    ),

    path('<int:pk>/ledger/debit/', DebitSupplierLedgerFormView.as_view(), name='ledger_debit'),
    path('<int:pk>/ledger/credit/', CreditSupplierLedgerFormView.as_view(), name='ledger_credit'),
    path('<int:pk>/ledger/list/', SupplierLedgerListView.as_view(), name='ledger_list'),
    path('credit/delete/<int:pk>', views.DeleteSupplierCredit, name='credit_delete'),

    ]
