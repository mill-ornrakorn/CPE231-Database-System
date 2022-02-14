from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from .DBHelper import DBHelper

from report.models import *

def index(request):
    invoice_no = request.GET.get('inv','')
    data_report = dict()
    data_report['invoice'] = list(Invoice.objects.filter(invoice_no=invoice_no).select_related('customer_code').values('invoice_no', 'date', 'customer_code_id', 'customer_code__name','due_date','total','vat','amount_due'))
    data_report['invoice_line_item'] = list(InvoiceLineItem.objects.filter(invoice_no=invoice_no).values())
    #return JsonResponse(data_report)
    return render(request, 'report_data.html', data_report)

#from index2
#def index(request):
#    data = Data.objects.get(key='default')
#    data_report = dict()
#    data_report['default'] = data.value
#    data_report['data'] = list(Data.objects.all().values())
#    data_report['invoice'] = list(Invoice.objects.filter(invoice_no='INT100/20').values())
#    data_report['invoice_line_item'] = list(InvoiceLineItem.objects.filter(invoice_no='INT100/20').values())
#    return JsonResponse(data_report)

#from index1
#def index(request):
#    data = Data.objects.get(key='default')
#    data_report = dict()
#    data_report['default'] = data.value
#    return render(request, 'report_data.html', data_report)

#from lab4 ppt
#def index(request):
#    return render(request, 'index.html')

def ReportDebtCustomers(request):
    db = DBHelper()
    sql = """SELECT c.customer_code as "Customer Code"
            , c.name as "Customer Name"
            , c.credit_limit as "Credit Limit"
            , (amount_due_each_customer - paid_each_customer) as "Debt"
            FROM customer c
            JOIN (SELECT customer_code, SUM(amount_due) as "amount_due_each_customer" FROM invoice GROUP BY customer_code) a
            ON a.customer_code = c.customer_code
            JOIN (SELECT customer_code, SUM(total_received) as "paid_each_customer" FROM receipt GROUP BY customer_code) b
            ON a.customer_code = b.customer_code
            WHERE (amount_due_each_customer - paid_each_customer) > 0 """
    data, columns = db.fetch (sql)

    data_report = dict() # create empty dict
    data_report['data'] = CursorToDict (data,columns)
    data_report['column_name'] = columns

    return render(request, 'report_debt_customers.html', data_report) 

def ReportListAllReceipts(request):
    db = DBHelper()
    sql = """ SELECT r.receipt_no as "Receipt No", r.date as "Date", r.customer_code as "Customer Code" 
            , c.name as "Customer Name", r.payment_method as "Payment Method", r.payment_reference as "Payment Reference" 
            , r.total_received as "Total Received", r.remarks as "Remarks", i.invoice_no as "Invoice No"
            , i.date as "Invoice Date", i.amount_due as "Invoice Full Amount", rli.amount_paid_here as"Amount Paid Here"   
            FROM receipt r JOIN customer c ON r.customer_code = c.customer_code 
            JOIN receipt_line_item rli ON r.receipt_no = rli.receipt_no 
            JOIN invoice i ON rli.invoice_no = i.invoice_no """
    
    data, columns = db.fetch (sql)
    data_report = dict() # create empty dict
    data_report['data'] = CursorToDict (data,columns)
    data_report['column_name'] = columns

    return render(request, 'report_list_all_receipts.html', data_report)    

def ReportUnpaidInvoices(request):
    db = DBHelper()
    sql_1 = """ SELECT i.invoice_no as "Invoice No", i.date as "Invoice Date", c.name as "Customer Name", 
	        i.amount_due as "Invoice Amount Due", a.paid_each_invoice as "Invoice Amount Received", 
		    (amount_due - paid_each_invoice) as "Invoice Amount Not Paid"
            FROM invoice i JOIN customer c ON i.customer_code = c.customer_code
            JOIN (SELECT invoice_no, SUM(amount_paid_here) as "paid_each_invoice" FROM receipt_line_item GROUP BY invoice_no) a
	        ON i.invoice_no = a.invoice_no WHERE (amount_due - paid_each_invoice) > 0 """
    data_1, columns_1 = db.fetch (sql_1)
    
    sql_2 = """ SELECT COUNT(i.invoice_no) as "number of Invoices not paid", 
	        SUM(amount_due - paid_each_invoice) as "total of Invoice Amount Not Paid" 
            FROM invoice i JOIN (SELECT invoice_no, SUM(amount_paid_here) as "paid_each_invoice" FROM receipt_line_item GROUP BY invoice_no) a 
            ON i.invoice_no = a.invoice_no WHERE (amount_due - paid_each_invoice) > 0 """
    data_2, columns_2 = db.fetch (sql_2 )
    
    data_report = dict() # create empty dict
    data_report['data_1'] = CursorToDict (data_1,columns_1)
    data_report['column_name_1'] = columns_1
    data_report['data_2'] = CursorToDict (data_2,columns_2)
    data_report['column_name_2'] = columns_2

    return render(request, 'report_unpaid_invoices.html', data_report)  

def ReportListAllInvoices(request):
    db = DBHelper()
    data, columns = db.fetch ('SELECT i.invoice_no as "Invoice No", i.date as "Date" '
                            ' , i.customer_code as "Customer Code", c.name as "Customer Name" '
                            ' , i.due_date as "Due Date", i.total as "Total", i.vat as "VAT", i.amount_due as "Amount Due" '
                            ' , ili.product_code as "Product Code", p.name as "Product Name" '
                            ' , ili.quantity as "Quantity", ili.unit_price as "Unit Price", ili.extended_price as "Extended Price" '
                            ' FROM invoice i JOIN customer c ON i.customer_code = c.customer_code '
                            '  JOIN invoice_line_item ili ON i.invoice_no = ili.invoice_no '
                            '  JOIN product p ON ili.product_code = p.code '
                            ' ')
    data_report = dict() # create empty dict
    data_report['data'] = CursorToDict (data,columns)
    data_report['column_name'] = columns

    return render(request, 'report_list_all_invoices.html', data_report)

def ReportProductsSold(request):
    db = DBHelper()
    data, columns = db.fetch ('SELECT ili.product_code as "Product Code", p.name as "Product Name" '
                              ' , SUM(ili.quantity) as "Total Quantity Sold", SUM(ili.extended_price) as "Total Value Sold" '
                              ' FROM invoice i JOIN invoice_line_item ili ON i.invoice_no = ili.invoice_no '
                              '   JOIN product p ON ili.product_code = p.code '
                              ' GROUP BY p.code, ili.product_code, p.name '
                            ' ')
    data_report = dict()
    data_report['data'] = CursorToDict (data,columns)
    data_report['column_name'] = columns

    return render(request, 'report_products_sold.html', data_report)

def ReportListAllProducts(request):
    db = DBHelper()
    data, columns = db.fetch ('SELECT code as "Code", name as "Name", units as "Units" FROM product '
                              ' ')
    data_report = dict()
    data_report['data'] = CursorToDict (data,columns)
    data_report['column_name'] = columns

    return render(request, 'report_list_all_products.html', data_report)

#เปลี่ยนเว้นวรรค เป็น _ เปลี่ยนอักษรพิมพ์ใหญ่เป็นพิมพ์เล็ก
def CursorToDict(data,columns): 
    result = []
    fieldnames = [name.replace(" ", "_").lower() for name in columns]
    for row in data:
        rowset = []
        for field in zip(fieldnames, row):
            rowset.append(field)
        result.append(dict(rowset))
    return result