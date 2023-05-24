import datetime

from django.db import models



class Product(models.Model):
    product_name = models.CharField(max_length=255)
    product_unit = models.CharField(default='ea', max_length=255)
    product_vendor = models.CharField(max_length=255, blank=True)
    product_is_delete = models.BooleanField(default=False)

    invoice = models.ForeignKey('Invoice', on_delete=models.CASCADE, null=True, blank=True)

    class Material(models.TextChoices):
        NATURAL_QUARTZITE = 'NATURAL QUARTZITE', 'Natural Quartzite'
        ENGINEERED_QUARTZ = 'ENGINEERED QUARTZ', 'Engineered Quartz'
        GRANITE = 'GRANITE', 'Granite'
        MARBLE = 'MARBLE', 'Marble'
        DOLOMITE = 'DOLOMITE', 'Dolomite'
        SOAPSTONE = 'SOAPSTONE', 'Soapstone'
        OTHER = 'OTHER', 'Other'
    product_material = models.CharField(max_length=255, choices=Material.choices, blank=True)

    def __str__(self):
        return str(self.product_name)


class ProductDetail(models.Model):
    product_qty = models.DecimalField(default=0, decimal_places=2, max_digits=9)
    product_price = models.DecimalField(default=0, decimal_places=2, max_digits=9)
    product_total = models.DecimalField(default=0, decimal_places=2, max_digits=10)

    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)


class Customer(models.Model):
    first_name = models.CharField('First Name', max_length=55, blank=True)
    last_name = models.CharField('Last Name', max_length=55, blank=True)
    phone = models.CharField('Phone Number', max_length=10, blank=True)
    alt_phone = models.CharField('Alt Phone Number', max_length=10, blank=True)
    company = models.CharField('Company', max_length=55, blank=True)
    email = models.EmailField('Email', null=True, blank=True)
    address = models.CharField('Address', max_length=55, blank=True)
    city = models.CharField('City', max_length=55, blank=True)
    state = models.CharField('State', max_length=55, blank=True)
    zip = models.CharField('Zip Code', max_length=9, blank=True)
    customer_notes = models.TextField(blank=True)
    date_created = models.DateTimeField(auto_created=True, null=True, blank=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Contractor(models.Model):
    contractor_first_name = models.CharField('Contractor First Name', max_length=55, blank=True)
    contractor_last_name = models.CharField('Contractor Last Name', max_length=55, blank=True)
    contractor_company = models.CharField('Contractor Company', max_length=55, blank=True)
    contractor_phone = models.CharField('Contractor Phone', max_length=11, blank=True)
    contractor_email = models.EmailField('Contractor Email', null=True, blank=True)

    contractor_address = models.CharField('Contractor Address', max_length=55, blank=True)
    contractor_city = models.CharField('Contractor City', max_length=55, blank=True)
    contractor_state = models.CharField('Contractor State', max_length=55, blank=True)
    contractor_zip = models.CharField('Contractor Zip Code', max_length=9, blank=True)
    contractor_notes = models.TextField(blank=True)


# class Job(models.Model):
#     job_name = models.CharField('Job Name', blank=True)
#     job_address = models.CharField('Job Address', blank=True)
#     job_city = models.CharField('Job City', blank=True)
#     job_state = models.CharField('State', blank=True)
#     job_zip = models.CharField('Zip Code', blank=True)


class Invoice(models.Model):
    class Status(models.TextChoices):
        BALANCE = 'BALANCE'
        PAID = 'PAID'
        CREDIT = 'CREDIT'

    class PaymentType(models.TextChoices):
        CASH = 'CASH'
        CHECK = 'CHECK'
        CARD = 'CARD'

    # invoice_date_created = models.DateTimeField(auto_now_add=True, default=datetime.datetime.now())
    invoice_date_created = models.DateTimeField(default=datetime.datetime.now())
    payment_type = models.CharField('Payment Method', max_length=25, blank=True, choices=PaymentType.choices)
    payment_status = models.CharField('Payment Status', max_length=25, blank=True, choices=Status.choices)
    subtotal = models.DecimalField('Subtotal', decimal_places=2, max_digits=9, default=0)
    tax = models.DecimalField('Sales Tax', decimal_places=2, max_digits=9, default=0)
    total = models.DecimalField('Total', decimal_places=2, max_digits=9, default=0)
    deposit = models.DecimalField('Deposit', decimal_places=2, max_digits=9, default=0)
    balance = models.DecimalField('Balance', decimal_places=2, max_digits=9, default=0)
    invoice_notes = models.TextField('Notes', blank=True)


    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    contractor = models.ForeignKey(Contractor, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return str(self.id)

    def calculate_tax(self, tax_rate=.0775):
        return self.subtotal * tax_rate


class InvoiceDetail(models.Model):
    # invoice = models.ForeignKey(
    #     Invoice, on_delete=models.SET_NULL, blank=True, null=True)
    invoice = models.OneToOneField(
        Invoice,
        on_delete=models.CASCADE,
        primary_key=True
    )
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, blank=True, null=True)
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, blank=True, null=True)


    @property
    def get_total_bill(self):
        total = float(self.product.product_price) * float(self.amount)
        return total
