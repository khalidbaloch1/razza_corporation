from django.urls import path
from . import views
from .views import (
    AddPurchase, PurchaseList, PurchaseDetailTemplateView
)

urlpatterns = [
    path('add/purchase/', AddPurchase.as_view(), name='add'),
    path('list/', PurchaseList.as_view(), name='list'),
    path('detail/<int:pk>/', PurchaseDetailTemplateView.as_view(), name='detail'),
    path('delete/<int:pk>', views.deletePurchase, name='delete'),

]