from django.views.generic import ListView, FormView, UpdateView, DeleteView
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404


from .forms import (VehicleForm)
from .models import (Vehicle)


class AddVehicle(FormView):
    form_class = VehicleForm
    template_name = 'vehicle/add_vehicle.html'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('common:login'))

        return super(
            AddVehicle, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(reverse('vehicle:list'))

    def form_invalid(self, form):
        return super(AddVehicle, self).form_invalid(form)


class VehicleList(ListView):
    model = Vehicle
    template_name = 'vehicle/list_vehicle.html'
    paginate_by = 100
    ordering = 'name'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('common:login'))

        return super(
            VehicleList, self).dispatch(request, *args, **kwargs)


class DeleteVehicle(DeleteView):
    model = Vehicle
    success_url = reverse_lazy('vehicle:list')
    success_message = ''

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('common:login'))

        return super(
            DeleteVehicle, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        messages.success(request, 'Deleted Vehicle SuccessFully')
        return self.post(request, *args, **kwargs)
