"""razza_corporation URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', IndexView.as_view(), name='home'),
    path('', include(('common.urls', 'common'), namespace='common')),
    path('product/', include(('product.urls', 'product'), namespace='product')),
    path('vehicle/', include(('vehicle.urls', 'vehicle'), namespace='vehicle')),
    path('customer/', include(('customer.urls', 'customer'), namespace='customer')),
    path('supplier/', include(('supplier.urls', 'supplier'), namespace='supplier')),
    path('purchase/', include(('purchase.urls', 'purchase'), namespace='purchase')),
    path('sales/', include(('sales.urls', 'sales'), namespace='sales')),
    ]
