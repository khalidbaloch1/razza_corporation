# Generated by Django 3.2.12 on 2022-07-02 20:21

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product', '0001_initial'),
        ('customer', '0003_customercredit'),
        ('vehicle', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sales',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price_per_ton', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=65, null=True)),
                ('total_ton', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=65, null=True)),
                ('total_amount', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=65, null=True)),
                ('deduction', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=65, null=True)),
                ('actual_sale', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=65, null=True)),
                ('frieght_recieved', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=65, null=True)),
                ('sub_total', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=65, null=True)),
                ('balance', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=65, null=True)),
                ('advance_payment', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=65, null=True)),
                ('gst', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=65, null=True)),
                ('gst_sub_total', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=65, null=True)),
                ('paid_amount', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=65, null=True)),
                ('remaining_payment', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=65, null=True)),
                ('sale_date', models.DateField(blank=True, default=django.utils.timezone.now, null=True)),
                ('dated', models.DateField(blank=True, default=django.utils.timezone.now, null=True)),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sales_customer', to='customer.customer')),
                ('item', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sales_item', to='product.productcategory')),
                ('vehicle', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sales_vehicle', to='vehicle.vehicle')),
            ],
        ),
    ]