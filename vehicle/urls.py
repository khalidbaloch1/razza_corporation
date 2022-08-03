from django.urls import path
from .views import (
    AddVehicle, VehicleList, DeleteVehicle
)

urlpatterns = [
    path('add/vehicle/', AddVehicle.as_view(), name='add_vehicle'),
    path('list/', VehicleList.as_view(), name='list'),
    path('delete/<int:pk>/', DeleteVehicle.as_view(), name='delete'),

]