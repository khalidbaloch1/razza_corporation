from django.urls import path
from . import views
from .views import (
    AddSales, SalesList, SalesDetailTemplateView, SalesUpdateView
)

urlpatterns = [
    path('add/', AddSales.as_view(), name='add'),
    path('list/', SalesList.as_view(), name='list'),
    path('detail/<int:pk>/', SalesDetailTemplateView.as_view(), name='detail'),
    path('delete/<int:pk>', views.deleteSales, name='delete'),
    path('update/<int:pk>/', SalesUpdateView.as_view(), name='update'),
    path('sales/pdf/<int:pk>/', views.sales_payslip, name='sales-pdf'),

]