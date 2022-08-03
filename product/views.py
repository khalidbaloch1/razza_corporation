from django.views.generic import ListView, FormView, UpdateView, DeleteView
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404


from product.forms import (
    ProductCategoryForm
)
from product.models import (
    ProductCategory
)


class AddProductCategory(FormView):
    form_class = ProductCategoryForm
    template_name = 'product/add_product_category.html'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('common:login'))

        return super(
            AddProductCategory, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(reverse('product:list'))

    def form_invalid(self, form):
        return super(AddProductCategory, self).form_invalid(form)


class ProductList(ListView):
    model = ProductCategory
    template_name = 'product/product_list.html'
    paginate_by = 100
    ordering = 'product'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('common:login'))

        return super(
            ProductList, self).dispatch(request, *args, **kwargs)


class DeleteProduct(DeleteView):
    model = ProductCategory
    success_url = reverse_lazy('product:list')
    success_message = ''

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('common:login'))

        return super(
            DeleteProduct, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        messages.success(request, 'Deleted Product SuccessFully')
        return self.post(request, *args, **kwargs)
