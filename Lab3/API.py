from DBHelper import DBHelper
from helper_functions import *
#This file will contain all API functions calls exposed to outside world for users to use
#This file made by JapPapin if u copy this pls delete this line

# function about Product
def create_product(products, code, name, units):
    result = products.create(code, name, units)#returns error dictionary
    if result['Is Error']: #if error
        print(result['Error Message'])
    else:
        print('Product Create Success.')
    return result #send result for caller program to use

def read_product(products, code):
    result = products.read(code) #returns tuple of (error dict, data dict)
    if result[0]['Is Error']: #in case error
        print(result[0]['Error Message'])
    else:
        print(result[1])
    return result #send result for caller program to use

def update_product(products, code, newName, newUnits):
    result = products.update(code, newName, newUnits) #returns error dictionary
    if result['Is Error']: #if error
        print(result['Error Message'])
    else:
        print('Product Update Success.')
    return result #send result for caller program to use

def delete_product(products, code):
    result = products.delete(code)#returns error dictionary
    if result['Is Error']: #if error
        print(result['Error Message'])
    else:
        print('Product Delete Success.')
    return result #send result for caller program to use

def report_list_products(products):
    result = products.dump()
    printDictInCSVFormat(result, ('Code',), ('Name', 'Units'))
    return result #send result for caller program to use

# function about Customer 
def create_customer(customers, customerCode, customerName, address, creditLimit, country):
    result = customers.create(customerCode, customerName, address, creditLimit, country)#returns error dictionary
    if result['Is Error']: #if error
        print(result['Error Message'])
    else:
        print('Customer Create Success.')
    return result #send result for caller program to use

def read_customer(customers, customerCode):
    result = customers.read(customerCode) #returns tuple of (error dict, data dict)
    if result[0]['Is Error']: #in case error
        print(result[0]['Error Message'])
    else:
        print(result[1])
    return result #send result for caller program to use

def update_customer(customers, customerCode, newCustomerName, newAddress, newCreditLimit, newCountry):
    result = customers.update(customerCode, newCustomerName, newAddress, newCreditLimit, newCountry) #returns error dictionary
    if result['Is Error']: #if error
        print(result['Error Message'])
    else:
        print('Customer Update Success.')
    return result #send result for caller program to use

def delete_customer(customers, customerCode):
    result = customers.delete(customerCode)#returns error dictionary
    if result['Is Error']: #if error
        print(result['Error Message'])
    else:
        print('Customer Delete Success.')
    return result #send result for caller program to use

def report_list_all_customers(customers):
    result = customers.dump()
    printDictInCSVFormat(result, ('Customer Code',), ('Name', 'Address','Credit Limit', 'Country'))
    return result #send result for caller program to use

# function about PaymentMethods
def create_payment_method(PaymentMethods, code, name):
    result = PaymentMethods.create(code, name)
    if result['Is Error']:
        print(result['Error Message'])
    else:
        print('Payment Method Create Success.')
    return result 

def read_payment_method(PaymentMethods, code):
    result = PaymentMethods.read(code)
    if result[0]['Is Error']:
        print(result[0]['Error Message'])
    else:
        print(result[1])
    return result

def update_payment_method(PaymentMethods, code, newName):
    result = PaymentMethods.update(code, newName)
    if result['Is Error']:
        print(result['Error Message'])
    else:
        print('Payment Method Update Success.')
    return result

def delete_payment_method(PaymentMethods, code):
    result = PaymentMethods.delete(code)
    if result['Is Error']:
        print(result['Error Message'])
    else:
        print('Payment Method Delete Success.')
    return result

def report_list_payment_method(PaymentMethods):
    result = PaymentMethods.dump()
    print (result)
    return result

# function about Invoice 
def create_invoice(invoices, invoiceNo, invoiceDate, customerCode, dueDate, invoiceLineTuplesList):
    if invoiceDate == None:
        invoiceDate = 'null'
    else:
        invoiceDate = "'" + invoiceDate + "'"
    if dueDate == None:
        dueDate = 'null'
    else:
        dueDate = "'" + dueDate + "'"
    result = invoices.create(invoiceNo, invoiceDate, customerCode, dueDate, invoiceLineTuplesList)#returns error dictionary
    if result['Is Error']: #if error
        print(result['Error Message'])
    else:
        print('Invoice Create Success.')
    return result #send result for caller program to use

def read_invoice(invoices, invoiceNo):
    result = invoices.read(invoiceNo) #returns tuple of (error dict, data dict)
    if result[0]['Is Error']: #in case error
        print(result[0]['Error Message'])
    else:
        print(result[1])
    return result #send result for caller program to use

def update_invoice(invoices, invoiceNo, newInvoiceDate, newCustomerCode, newDueDate, newInvoiceLineTuplesList):
    if newInvoiceDate == None:
        newInvoiceDate = 'null'
    else:
        newInvoiceDate = "'" + newInvoiceDate + "'"
    if newDueDate == None:
        newDueDate = 'null'
    else:
        newDueDate = "'" + newDueDate + "'"
    result = invoices.update(invoiceNo, newInvoiceDate, newCustomerCode, newDueDate, newInvoiceLineTuplesList) #returns error dictionary
    if result['Is Error']: #if error
        print(result['Error Message'])
    else:
        print('Invoice Update Success.')
    return result #send result for caller program to use

def delete_invoice(invoices, invoiceNo):
    result = invoices.delete(invoiceNo)#returns error dictionary
    if result['Is Error']: #if error
        print(result['Error Message'])
    else:
        print('Invoice Delete Success.')
    return result #send result for caller program to use

def update_invoice_line(invoices, invoiceNo, productCode, newQuantity, newUnitPrice):
    result = invoices.update_invoice_line(invoiceNo, productCode, newQuantity, newUnitPrice) #returns error dictionary
    if result['Is Error']: #if error
        print(result['Error Message'])
    else:
        print('Invoice Line Item Update Success.')
    return result #send result for caller program to use

def delete_invoice_line(invoices, invoiceNo, productCode):
    result = invoices.delete_invoice_line(invoiceNo, productCode) #returns error dictionary
    if result['Is Error']: #if error
        print(result['Error Message'])
    else:
        print('Invoice Line Item Delete Success.')
    return result #send result for caller program to use

def report_list_all_invoices(invoices, customers, products):
    result = invoices.dump()
    printDictInCSVFormat(result, ('Invoice No : Product Code',), ('Date', 'Customer Code', 'Customer Name','Due Date','Total','VAT','Amount Due'
                                    , 'Product Name', 'Quantity', 'Unit Price', 'Extended Price'))
    return result #send result for caller program to use

# function about Receipt 
def create_receipt(Receipts, receiptNo, receiptDate, customerCode, paymentMethod, paymentReference, remarks, receiptLineTuplesList):
    if receiptDate == None:
        receiptDate = 'null'
    else:
        receiptDate = "'" + receiptDate + "'"
    result = Receipts.create(receiptNo, receiptDate, customerCode, paymentMethod, paymentReference, remarks, receiptLineTuplesList)
    if result['Is Error']:
        print(result['Error Message'])
    else:
        print('Receipt Create Success.')
    return result 

def read_receipt(Receipts, receiptNo):
    result = Receipts.read(receiptNo) 
    if result[0]['Is Error']:
        print(result[0]['Error Message'])
    else:
        print(result[1])
    return result

def update_receipt(Receipts, receiptNo, newReceiptDate, newCustomerCode, newPaymentMethod, newPaymentReference, newRemarks, newReceiptLineTuplesList):
    if newReceiptDate == None:
        newReceiptDate = 'null'
    else:
        newReceiptDate = "'" + newReceiptDate + "'"
    result = Receipts.update(receiptNo, newReceiptDate, newCustomerCode, newPaymentMethod, newPaymentReference, newRemarks, newReceiptLineTuplesList) 
    if result['Is Error']:
        print(result['Error Message'])
    else:
        print('Receipt Update Success.')
    return result

def delete_receipt(Receipts, receiptNo):
    result = Receipts.delete(receiptNo)
    if result['Is Error']: 
        print(result['Error Message'])
    else:
        print('Receipt Delete Success.')
    return result

def update_receipt_line(Receipts, receiptNo, invoiceNo, newAmountPaidHere):
    result = Receipts.update_receipt_line(receiptNo, invoiceNo, newAmountPaidHere)
    if result['Is Error']:
        print(result['Error Message'])
    else:
        print('Receipt Line Item Update Success.')
    return result 

def delete_receipt_line(Receipts, receiptNo, invoiceNo):
    result = Receipts.delete_receipt_line(receiptNo, invoiceNo)
    if result['Is Error']:
        print(result['Error Message'])
    else:
        print('Receipt Line Item Delete Success.')
    return result 

def report_list_all_receipts(receipts, invoices, customers):
    result = receipts.dump()
    printDictInCSVFormat(result, (None), ('Receipt No','Date', 'Customer Code', 'Customer Name','Payment Method','Payment Reference','Total Received','Remarks',
                                                'Invoice No', 'Invoice Date', 'Invoice Full Amount', 'Amount Paid Here'))
    return result 

def report_unpaid_invoices(invoices, customers, receipts):
    db = DBHelper()
    sql_1 = """SELECT i.invoice_no as "Invoice No", i.date as "Invoice Date", c.name as "Customer Name", 
	        i.amount_due as "Invoice Amount Due", a.paid_each_invoice as "Invoice Amount Received", 
		    (amount_due - paid_each_invoice) as "Invoice Amount Not Paid"
            FROM invoice i JOIN customer c ON i.customer_code = c.customer_code
            JOIN (SELECT invoice_no, SUM(amount_paid_here) as "paid_each_invoice" FROM receipt_line_item GROUP BY invoice_no) a
	        ON i.invoice_no = a.invoice_no WHERE (amount_due - paid_each_invoice) > 0 """
    data, columns = db.fetch (sql_1)
    result_1 = row_as_dict(data, columns)
    data, columns = db.fetch ('SELECT 0 as "Footer", COUNT(i.invoice_no) as "number of Invoices not paid", ' 
	                          ' SUM(amount_due - paid_each_invoice) as "total of Invoice Amount Not Paid" '
                              ' FROM invoice i JOIN (SELECT invoice_no, SUM(amount_paid_here) as "paid_each_invoice" FROM receipt_line_item GROUP BY invoice_no) a '
                              ' ON i.invoice_no = a.invoice_no WHERE (amount_due - paid_each_invoice) > 0' )
    result_2 = row_as_dict(data, columns)
    printDictInCSVFormat(result_1, ('Invoice No',), ('Invoice Date', 'Customer Name', 'Invoice Amount Due', 'Invoice Amount Received', 'Invoice Amount Not Paid'))
    printDictInCSVFormat(result_2,(None), ('number of Invoices not paid', 'total of Invoice Amount Not Paid'))
    return result_1,result_2

def report_products_sold(invoices, products, dateStart, dateEnd):
    # Will return 2 dictionaries: 
    # 1) a dictionary as list of in products sold in the given date range in tabular format of: Product Code, Product Name, Total Quantity Sold, Total Value Sold. Here, (product code) will be unique. 
    # And 2) a second dictionary of the footer will also be returned containing: t the end also show the sum of Total Value Sold.  
    db = DBHelper()
    data, columns = db.fetch ('SELECT p.code as "Code", ili.product_code as "Product Code", p.name as "Product Name" '
                              ' , SUM(ili.quantity) as "Total Quantity Sold", SUM(ili.extended_price) as "Total Value Sold" '
                              ' FROM invoice i JOIN invoice_line_item ili ON i.invoice_no = ili.invoice_no '
                              '   JOIN product p ON ili.product_code = p.code '
                              ' WHERE i.date between \'' + dateStart + '\' and \'' + dateEnd + '\' '
                              ' GROUP BY p.code, ili.product_code, p.name ')
    result = row_as_dict(data, columns)
    data, columns = db.fetch ('SELECT 0 as "Footer", SUM(ili.extended_price) as "Total Value Sold" '
                              ' FROM invoice i JOIN invoice_line_item ili ON i.invoice_no = ili.invoice_no '
                              '   JOIN product p ON ili.product_code = p.code '
                              ' WHERE i.date between \'' + dateStart + '\' and \'' + dateEnd + '\' '
                              ' ')
    result2 = row_as_dict(data, columns)

    printDictInCSVFormat(result, (None), ('Product Code','Product Name', 'Total Quantity Sold', 'Total Value Sold'))
    printDictInCSVFormat(result2, (None), ('Total Value Sold',))
    return result, result2

def report_customer_products_sold_list(invoices, products, customers, dateStart, dateEnd):
    # Will return 2 dictionaries: 
    # 1) a dictionary as list of customers and list the products sold to them in the given date range in this format:  Customer Code, Customer Name, Product Code,  Product Name, Invoice No, Invoice Date, Quantity Sold, Value Sold. Here, (customer code, product code, invoice no) will be unique.  
    # And 2) a second footer dictionary showing:  At the end also show the sum of Quantity Sold and sum of Value Sold.
    db = DBHelper()
    data, columns = db.fetch ('SELECT i.customer_code, c.customer_code as "Customer Code", c.name as "Customer Name" '
                              ' , ili.product_code as "Product Code", p.name as "Product Name" '
                              ' , i.invoice_no as "Invoice No" '
                              ' , SUM(ili.quantity) as "Quantity Sold", SUM(ili.extended_price) as "Value Sold" '
                              ' FROM invoice i JOIN invoice_line_item ili ON i.invoice_no = ili.invoice_no '
                              '   JOIN customer c ON i.customer_code = c.customer_code '
                              '   JOIN product p ON ili.product_code = p.code '
                              ' WHERE i.date between \'' + dateStart + '\' and \'' + dateEnd + '\' '
                              ' GROUP BY i.customer_code, c.customer_code, c.name, i.invoice_no, ili.product_code, p.name ')
    result = row_as_dict(data, columns)
    data, columns = db.fetch ('SELECT 0 as "Footer", SUM(ili.quantity) as "Quantity Sold", SUM(ili.extended_price) as "Value Sold" '
                              ' FROM invoice i JOIN invoice_line_item ili ON i.invoice_no = ili.invoice_no '
                              '   JOIN customer c ON i.customer_code = c.customer_code '
                              '   JOIN product p ON ili.product_code = p.code '
                              ' WHERE i.date between \'' + dateStart + '\' and \'' + dateEnd + '\' '
                              ' ')
    result2 = row_as_dict(data, columns)

    printDictInCSVFormat(result, (None), ('Customer Code','Customer Name', 'Product Code', 'Product Name', 'Invoice No', 'Quantity Sold', 'Value Sold'))
    printDictInCSVFormat(result2, (None), ('Quantity Sold','Value Sold'))
    return result.values(), result2

def report_customer_products_sold_total(invoices, products, customers, dateStart, dateEnd):
    # Will return 2 dictionaries: 
    # 1) a dictionary as list customers and the total number and value of products sold to them in the given date range in this format:  Customer Code, Customer Name, Product Code,  Product Name, Total Quantity Sold, Total Value Sold. Here (customer code, product code) will be unique.
    # And 2) a second footer dictionary showing: t the end also show the sum of Total Quantity Sold, sum of Total Value Sold.
    db = DBHelper()
    data, columns = db.fetch ('SELECT i.customer_code, c.customer_code as "Customer Code", c.name as "Customer Name" '
                              ' , ili.product_code as "Product Code", p.name as "Product Name" '
                              ' , SUM(ili.quantity) as "Total Quantity Sold", SUM(ili.extended_price) as "Total Value Sold" '
                              ' FROM invoice i JOIN invoice_line_item ili ON i.invoice_no = ili.invoice_no '
                              '   JOIN customer c ON i.customer_code = c.customer_code '
                              '   JOIN product p ON ili.product_code = p.code '
                              ' WHERE i.date between \'' + dateStart + '\' and \'' + dateEnd + '\' '
                              ' GROUP BY i.customer_code, c.customer_code, c.name, i.invoice_no, ili.product_code, p.name ')
    result = row_as_dict(data, columns)
    data, columns = db.fetch ('SELECT 0 as "Footer", SUM(ili.quantity) as "Total Quantity Sold", SUM(ili.extended_price) as "Total Value Sold" '
                              ' FROM invoice i JOIN invoice_line_item ili ON i.invoice_no = ili.invoice_no '
                              '   JOIN customer c ON i.customer_code = c.customer_code '
                              '   JOIN product p ON ili.product_code = p.code '
                              ' WHERE i.date between \'' + dateStart + '\' and \'' + dateEnd + '\' '
                              ' ')
    result2 = row_as_dict(data, columns)

    printDictInCSVFormat(result, (None), ('Customer Code','Customer Name', 'Product Code', 'Product Name', 'Total Quantity Sold', 'Total Value Sold'))
    printDictInCSVFormat(result2, (None), ('Total Quantity Sold','Total Value Sold'))
    return result.values(), result2