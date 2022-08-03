from django import forms
from product.models import (
    ProductCategory
)


class ProductCategoryForm(forms.ModelForm):
    class Meta:
        model = ProductCategory
        fields = '__all__'
