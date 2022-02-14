from django.db import models

# Create your models here.
class Customer(models.Model):
    customer_code = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    credit_limit = models.FloatField(null=True, blank=True)
    country = models.CharField(max_length=20, null=True, blank=True)
    
    class Meta:
        db_table = "customer"
        managed = False
    def __str__(self):
        return self.customer_code

class Invoice(models.Model):
    invoice_no = models.CharField(max_length=10, primary_key=True)
    date = models.DateField(null=True)
    customer_code = models.ForeignKey(Customer, on_delete=models.CASCADE, db_column='customer_code')
    due_date = models.DateField(null=True, blank=True)
    total = models.FloatField(null=True, blank=True)
    vat = models.FloatField(null=True, blank=True)
    amount_due = models.FloatField(null=True, blank=True)

    class Meta:
        db_table = "invoice"
        managed = False
    def __str__(self):
        return self.invoice_no

class PaymentMethod(models.Model):
    payment_code = models.CharField(max_length=20, primary_key=True)
    payment_name = models.CharField(max_length=100, null=True)

    class Meta:
        db_table = "payment_method"
        managed = False
    def __str__(self):
        return self.payment_code

class Receipt(models.Model):
    receipt_no = models.CharField(max_length=10, primary_key=True)
    date = models.DateField(null=True)
    customer_code = models.ForeignKey(Customer, on_delete=models.CASCADE, db_column='customer_code')
    payment_code = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE, db_column='payment_code')
    payment_reference = models.CharField(max_length=100, null=True, blank=True)
    total_received = models.FloatField(null=True, blank=True)
    remarks = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        db_table = "receipt"
        managed = False

class ReceiptLineItem(models.Model):
    lineitem = models.IntegerField()
    receipt_no = models.ForeignKey(Receipt, on_delete=models.CASCADE, db_column='receipt_no')
    invoice_no = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='invoice_number', db_column='invoice_no')
    amount_paid_here = models.FloatField(null=True)

    class Meta:
        db_table = "receipt_line_item"
        unique_together = (("lineitem", "receipt_no"),)
        managed = False



