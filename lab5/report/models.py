from django.db import models

# Create your models here.
class Data(models.Model):
    key = models.CharField(max_length=10,primary_key=True)
    value = models.CharField(max_length=100)

class Product(models.Model):
    code = models.CharField(max_length=10,primary_key=True)
    name = models.CharField(max_length=100)
    units = models.CharField(max_length=10)
    class Meta:
        db_table = "product"
        managed = False

class Customer(models.Model):
    customer_code = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    credit_limit = models.FloatField(null=True, blank=True)
    country = models.CharField(max_length=20, null=True, blank=True)
    class Meta:
        db_table = "customer"
        managed = False

class Invoice(models.Model):
    invoice_no = models.CharField(max_length=10, primary_key=True)
    date = models.DateField(null=True)
    customer_code = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='customer', db_column='customer_code')
    due_date = models.DateField(null=True, blank=True)
    total = models.FloatField(null=True, blank=True)
    vat = models.FloatField(null=True, blank=True)
    amount_due = models.FloatField(null=True, blank=True)
    class Meta:
        db_table = "invoice"
        managed = False

class InvoiceLineItem(models.Model):
    invoice_no = models.ForeignKey(Invoice, primary_key=True, on_delete=models.CASCADE, db_column='invoice_no')
    product_code = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product', db_column='product_code')
    quantity = models.IntegerField(null=True)
    unit_price = models.FloatField(null=True)
    extended_price = models.FloatField(null=True)
    class Meta:
        db_table = "invoice_line_item"
        unique_together = (("invoice_no", "product_code"),)
        managed = False

class Receipt(models.Model):
    receipt_no = models.CharField(max_length=10, primary_key=True)
    date = models.DateField(null=True)
    customer_code = models.ForeignKey(Customer, on_delete=models.CASCADE, db_column='customer_code')
    total_received = models.FloatField(null=True, blank=True)
    remarks = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        db_table = "receipt"
        managed = False

class ReceiptLineItem(models.Model):
    lineitem = models.IntegerField()
    receipt_no = models.ForeignKey(Receipt, on_delete=models.CASCADE, db_column='receipt_no')
    invoice_no = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='invoice_number', db_column='invoice_no')
    invoice_date = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='invoice_date', db_column='date')
    invoice_full_amount = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='invoice_full_amount', db_column='amount_due')
    invoice_amount_remain = models.FloatField(null=True)
    amount_paid_here = models.FloatField(null=True)

    class Meta:
        db_table = "receipt_line_item"
        unique_together = (("lineitem", "receipt_no"),)
        managed = False

class PaymentMethod(models.Model):
    code = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=100, null=True)

    class Meta:
        db_table = "payment_method"
        managed = False
    def __str__(self):
        return self.code