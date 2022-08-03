from django.db import models
from django.db.models.signals import pre_delete
from django.utils import timezone
from django.db.models import Sum
from customer.models import Customer
from product.models import ProductCategory
from vehicle.models import Vehicle


class Sales(models.Model):
        item = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, null=True, blank=True, related_name='sales_item')
        vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, null=True, blank=True, related_name='sales_vehicle')
        customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True, related_name='sales_customer')
        price_per_ton = models.DecimalField(max_digits=65, decimal_places=2, default=0, null=True, blank=True)
        total_ton = models.DecimalField(max_digits=65, decimal_places=2, default=0, null=True, blank=True)
        total_amount = models.DecimalField(max_digits=65, decimal_places=2, default=0, null=True, blank=True)
        deduction = models.DecimalField(max_digits=65, decimal_places=2, default=0, null=True, blank=True)
        actual_sale = models.DecimalField(max_digits=65, decimal_places=2, default=0, null=True, blank=True)
        frieght_recieved = models.DecimalField(max_digits=65, decimal_places=2, default=0, null=True, blank=True)
        sub_total = models.DecimalField(max_digits=65, decimal_places=2, default=0, null=True, blank=True)
        balance = models.DecimalField(max_digits=65, decimal_places=2, default=0, null=True, blank=True)
        advance_payment = models.DecimalField(max_digits=65, decimal_places=2, default=0, null=True, blank=True)
        gst = models.DecimalField(max_digits=65, decimal_places=2, default=0, null=True, blank=True)
        gst_sub_total = models.DecimalField(max_digits=65, decimal_places=2, default=0, null=True, blank=True)
        paid_amount = models.DecimalField(max_digits=65, decimal_places=2, default=0, null=True, blank=True)
        remaining_payment = models.DecimalField(max_digits=65, decimal_places=2, default=0, null=True, blank=True)
        bilty_no = models.CharField(max_length=100, null=True, blank=True)
        sale_date = models.DateField(default=timezone.now, null=True, blank=True)
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

    from customer.models import CustomerLedger
    CustomerLedger.objects.filter(
        details='Remaining Payment for Bilty No. %s and'
                ' Sales %d.' % (instance.bilty_no, instance.id)
    ).delete()


# Signals
pre_delete.connect(delete_all_details, sender=Sales)
