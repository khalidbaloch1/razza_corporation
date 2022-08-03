from django.db import models
from django.utils import timezone
from django.db.models.signals import pre_delete
from product.models import ProductCategory
from vehicle.models import Vehicle
from supplier.models import Supplier


class Purchase(models.Model):
        item = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, null=True, blank=True, related_name='purchase_item')
        vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, null=True, blank=True, related_name='purchase_vehicle')
        supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, null=True, blank=True, related_name='purchase_supplier')
        price_per_ton = models.DecimalField(max_digits=65, decimal_places=2, default=0, null=True, blank=True)
        total_ton = models.DecimalField(max_digits=65, decimal_places=2, default=0, null=True, blank=True)
        advance_payment = models.DecimalField(max_digits=65, decimal_places=2, default=0, null=True, blank=True)
        after_advance_payment = models.DecimalField(max_digits=65, decimal_places=2, default=0, null=True, blank=True)
        total_expense = models.DecimalField(max_digits=65, decimal_places=2, default=0, null=True, blank=True)
        frieght = models.DecimalField(max_digits=65, decimal_places=2, default=0, null=True, blank=True)
        cost = models.DecimalField(max_digits=65, decimal_places=2, default=0, null=True, blank=True)
        total_cost = models.DecimalField(max_digits=65, decimal_places=2, default=0, null=True, blank=True)
        bilty_details = models.CharField(max_length=100, null=True, blank=True)
        bilty_no = models.CharField(max_length=100, null=True, blank=True)
        bilty_image = models.ImageField(upload_to="bilty/img/", null=True, blank=True)
        purchase_date = models.DateField(default=timezone.now, null=True, blank=True)
        dated = models.DateField(default=timezone.now, blank=True, null=True)

        def __str__(self):
            return self.bilty_no or ''


# Signal Functions
def delete_all_details(instance, **kwargs):
    """
    The functions used to check if user profile is not created
    and created the user profile without saving role and hospital
    :param sender:
    :param instance:
    :param created:
    :param kwargs:
    :return:
    """
    # if created and not UserProfile.objects.filter(user=instance):
    #     return UserProfile.objects.create(
    #         user=instance,
    #         user_type=UserProfile.USER_TYPE_OWNER
    #     )

    from supplier.models import SupplierLedger
    SupplierLedger.objects.filter(
        details='Remaining Payment for Bilty No. %s and'
                ' Purchase %d.' % (instance.bilty_no, instance.id)
    ).delete()


# Signals
pre_delete.connect(delete_all_details, sender=Purchase)
