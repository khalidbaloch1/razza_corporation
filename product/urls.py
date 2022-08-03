from django.urls import path
from product.views import (
    AddProductCategory, ProductList, DeleteProduct
)

urlpatterns = [
    path('add/category/', AddProductCategory.as_view(), name='add_category'),
    path('list/', ProductList.as_view(), name='list'),
    path('delete/<int:pk>/', DeleteProduct.as_view(), name='delete'),

]