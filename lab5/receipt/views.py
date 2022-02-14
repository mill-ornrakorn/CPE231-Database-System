from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic import View
from django.http import JsonResponse
from django import forms
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.forms.models import model_to_dict
from django.db.models import Max
from django.db import connection
from receipt.models import *
from invoice.models import *
import json

# Create your views here.
def index(request):
    data = {}
    return render(request, 'receipt/receipt.html', data)

class PaymentMethodDetail(View):
    def get(self, request, pk):
        paymentmethod = get_object_or_404(PaymentMethod, pk=pk)
        data = dict()
        data['paymentmethods'] = model_to_dict(paymentmethod)
        response = JsonResponse(data)
        response["Access-Control-Allow-Origin"] = "*"
        return response

class ReciptListInvoice(View):
    def get(self, request):

        sql = """SELECT i.invoice_no, i.date as invoice_date, i.amount_due as invoice_full_amount
                , COALESCE((SELECT i.amount_due - SUM(rli2.amount_paid_here) 
			    FROM receipt_line_item as rli2 WHERE rli2.invoice_no = i.invoice_no), i.amount_due) as invoice_amount_remain
                , COALESCE(SUM(rli.amount_paid_here), 0 ) as amount_paid_here
                FROM invoice as i LEFT JOIN receipt_line_item rli ON i.invoice_no = rli.invoice_no 
				GROUP BY i.invoice_no ORDER BY i.invoice_no  """
        
        with connection.cursor() as cursor:
                cursor.execute(sql)
                receiptlistinvoice = dictfetchall(cursor)
        
        data = dict()
        data['receiptlistinvoice'] = receiptlistinvoice
        response = JsonResponse(data)
        response["Access-Control-Allow-Origin"] = "*"
        return response    

class PaymentMethodList(View):
    def get(self, request):
        paymentmethods = list(PaymentMethod.objects.all().values())
        data = dict()
        data['paymentmethods'] = paymentmethods
        response = JsonResponse(data)
        response["Access-Control-Allow-Origin"] = "*"
        return response        

class ReceiptList(View):
    def get(self, request):
        receipts = list(Receipt.objects.order_by('receipt_no').all().values())
        data = dict()
        data['receipts'] = receipts
        response = JsonResponse(data)
        response["Access-Control-Allow-Origin"] = "*"
        return response       

class ReceiptDetail(View):
    def get(self, request, pk, pk2):
        receipt_no = pk + "/" + pk2

        receipt = list(Receipt.objects.select_related("customer").filter(receipt_no=receipt_no).values('receipt_no', 
                'date', 'customer_code', 'customer_code__name','payment_code_id', 'payment_reference', 'total_received', 'remarks'))
        sql =  """SELECT rli.lineitem, rli.receipt_no, rli.invoice_no, i.date as invoice_date, i.amount_due as invoice_full_amount
            , (SELECT i.amount_due - SUM(rli2.amount_paid_here) FROM receipt_line_item as rli2 WHERE rli2.invoice_no = i.invoice_no) as invoice_amount_remain
            , rli.amount_paid_here FROM receipt_line_item as rli LEFT JOIN invoice as i on rli.invoice_no = i.invoice_no WHERE rli.receipt_no = '{}' """.format(receipt_no)

        with connection.cursor() as cursor:
                cursor.execute(sql)
                receiptlineitem = dictfetchall(cursor)

        data = dict()
        data['receipt'] = receipt[0]
        data['receiptlineitem'] = receiptlineitem
        
        response = JsonResponse(data)
        response["Access-Control-Allow-Origin"] = "*"
        return response

class ReceiptForm(forms.ModelForm):
    class Meta:
        model = Receipt
        fields = '__all__'  

class ReceiptLineItemForm(forms.ModelForm):
    class Meta:
        model = ReceiptLineItem
        fields = '__all__'

@method_decorator(csrf_exempt, name='dispatch')
class ReceiptCreate(View):
    def post(self, request):
        data = dict()
        request.POST = request.POST.copy()
        if Receipt.objects.count() != 0:
            receipt_no_max = Receipt.objects.aggregate(Max('receipt_no'))['receipt_no__max']
            next_receipt_no = receipt_no_max[0:3] + str(int(receipt_no_max[3:7])+1) + "/" + receipt_no_max[8:10]
        else:
            next_receipt_no = "RCT1001/20"
        request.POST['receipt_no'] = next_receipt_no
        request.POST['date'] = reFormatDateMMDDYYYY(request.POST['date'])
        request.POST['payment_reference'] = request.POST['payment_reference']
        request.POST['total_received'] = reFormatNumber(request.POST['total_received'])
        request.POST['remarks'] = request.POST['remarks']

        form = ReceiptForm(request.POST)
        if form.is_valid():
            receipt = form.save()

            dict_lineitem = json.loads(request.POST['lineitem'])
            for lineitem in dict_lineitem['lineitem']:
                lineitem['receipt_no'] = next_receipt_no
                lineitem['amount_paid_here'] = reFormatNumber(lineitem['amount_paid_here'])

                formlineitem = ReceiptLineItemForm(lineitem)
                formlineitem.save()

            data['receipt'] = model_to_dict(receipt)
        else:
            data['error'] = 'form not valid!'

        response = JsonResponse(data)
        response["Access-Control-Allow-Origin"] = "*"
        return response      

@method_decorator(csrf_exempt, name='dispatch')
class ReceiptUpdate(View):
    def post(self, request, pk, pk2):
        receipt_no = pk + "/" + pk2
        data = dict()
        receipt = Receipt.objects.get(pk=receipt_no)
        request.POST = request.POST.copy()
        request.POST['receipt_no'] = receipt_no
        request.POST['date'] = reFormatDateMMDDYYYY(request.POST['date'])
        request.POST['payment_reference'] = request.POST['payment_reference']
        request.POST['total_received'] = reFormatNumber(request.POST['total_received'])
        request.POST['remarks'] = request.POST['remarks']

        form = ReceiptForm(instance=receipt, data=request.POST)
        if form.is_valid():
            receipt = form.save()

            ReceiptLineItem.objects.filter(receipt_no=receipt_no).delete()

            dict_lineitem = json.loads(request.POST['lineitem'])
            for lineitem in dict_lineitem['lineitem']:
                lineitem['receipt_no'] = receipt_no
                lineitem['amount_paid_here'] = reFormatNumber(lineitem['amount_paid_here'])

                formlineitem = ReceiptLineItemForm(lineitem)
                formlineitem.save()

            data['receipt'] = model_to_dict(receipt)
        else:
            data['error'] = 'form not valid!'

        response = JsonResponse(data)
        response["Access-Control-Allow-Origin"] = "*"
        return response

@method_decorator(csrf_exempt, name='dispatch')
class ReceiptDelete(View):
    def post(self, request, pk, pk2):
        receipt_no = pk + "/" + pk2
        data = dict()
        receipt = Receipt.objects.get(pk=receipt_no)
        if receipt:
            receipt.delete()
            data['message'] = "Receipt Deleted!"
        else:
            data['message'] = "Error!"

        return JsonResponse(data)

class ReceiptPDF(View):
    def get(self, request, pk, pk2):
        receipt_no = pk + "/" + pk2

        receipt = list(Receipt.objects.select_related("custome").filter(receipt_no=receipt_no).values('receipt_no', 
                'date', 'customer_code', 'customer_code__name','payment_code_id', 'payment_code__payment_name', 'payment_reference', 'total_received', 'remarks'))
        sql =  """SELECT rli.lineitem, rli.receipt_no, rli.invoice_no, i.date as invoice_date, i.amount_due as invoice_full_amount
            , (SELECT i.amount_due - SUM(rli2.amount_paid_here) FROM receipt_line_item as rli2 WHERE rli2.invoice_no = i.invoice_no) as invoice_amount_remain
            , rli.amount_paid_here FROM receipt_line_item as rli LEFT JOIN invoice as i on rli.invoice_no = i.invoice_no WHERE rli.receipt_no = '{}' """.format(receipt_no)

        with connection.cursor() as cursor:
                cursor.execute(sql)
                receiptlineitem = dictfetchall(cursor)

        data = dict()
        data['receipt'] = receipt[0]
        data['receiptlineitem'] = receiptlineitem

        #return JsonResponse(data)
        return render(request, 'receipt/pdf.html', data)

class ReceiptReport(View):
    def get(self, request):

        with connection.cursor() as cursor:
            sql = """ SELECT r.receipt_no as "Receipt No", r.date as "Date", r.customer_code as "Customer Code" 
                , c.name as "Customer Name", r.payment_method as "Payment Method", r.payment_reference as "Payment Reference" 
                , r.total_received as "Total Received", r.remarks as "Remarks"  
                FROM receipt r JOIN customer c ON r.customer_code = c.customer_code 
                JOIN receipt_line_item rli ON r.receipt_no = rli.receipt_no 
                JOIN invoice i ON rli.invoice_no = i.invoice_no """

            cursor.execute(sql)
            
            row = dictfetchall(cursor)
            column_name = [col[0] for col in cursor.description]

        data = dict()
        data['column_name'] = column_name
        data['data'] = row
        
        #return JsonResponse(data)
        return render(request, 'receipt/report.html', data)

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [name[0].replace(" ", "_").lower() for name in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def reFormatDateMMDDYYYY(ddmmyyyy):
        if (ddmmyyyy == ''):
            return ''
        return ddmmyyyy[3:5] + "/" + ddmmyyyy[:2] + "/" + ddmmyyyy[6:]

def reFormatNumber(str):
        if (str == ''):
            return ''
        return str.replace(",", "")
