from helper_functions import *
#This file will contain all API functions calls exposed to outside world for users to use

# function about Product
def create_payment_method(paymentMethod, code, name):
    result = paymentMethod.create(code, name)#returns error dictionary
    if result['Is Error']: #if error
        print(result['Error Message'])
    else:
        print('Product Create Success.')
    return result #send result for caller program to use

def read_payment_method(paymentMethod, code):
    result = paymentMethod.read(code) #returns tuple of (error dict, data dict)
    if result[0]['Is Error']: #in case error
        print(result[0]['Error Message'])
    else:
        print(result[1])
    return result #send result for caller program to use

def update_payment_method(paymentMethod, code, newName):
    result = paymentMethod.update(code, newName) #returns error dictionary
    if result['Is Error']: #if error
        print(result['Error Message'])
    else:
        print('Product Update Success.')
    return result #send result for caller program to use

def delete_payment_method(paymentMethod, code):
    result = paymentMethod.delete(code)#returns error dictionary
    if result['Is Error']: #if error
        print(result['Error Message'])
    else:
        print('Product Delete Success.')
    return result #send result for caller program to use

def report_list_payment_method(paymentMethod):
    result = paymentMethod.dump()
    #printDictInCSVFormat(result, ('Code',), ('Name', 'Units'))
    print (result)
    return result #send result for caller program to use

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
    #printDictInCSVFormat(result, ('Code',), ('Name', 'Units'))
    print (result)
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

# function about Invoice 
def create_invoice(invoices, invoiceNo, invoiceDate, customerCode, dueDate, invoiceLineTuplesList):
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
    # Will dump all invoices data and return 1 dictionary as a result (with header and line item joined).  
    # Please show the customer name and product name also. 
    # A helper function such as def print_tabular_dictionary(tabularDictionary) can then be called to print this in a tabular (table-like) form with column headings and data. 

    allInvoice = invoices.dump()
    # re-format result by add Customer Name in object and Product Name in line item
    result = {}
    for invoiceNo, invoiceDetail in allInvoice.items():
        newValue = {}
        for invoiceColumn, invoiceData in invoiceDetail.items():
            if invoiceColumn == "Customer Code":
                newValue[invoiceColumn] = invoiceData
                customer = customers.read(invoiceDetail["Customer Code"])
                # if no found
                if customer[0]['Is Error']:
                    newValue["Customer Name"] = ""
                else:
                    newValue["Customer Name"] = customer[1]["Name"]

            elif invoiceColumn == "Items List":
                newLineItemList = []
                # info in Item List key of invoice
                for lineItem in invoiceDetail['Items List']:
                    newLineItemInv = {}
                    for lineItemColumn, lineItemData in lineItem.items():
                        if lineItemColumn == "Product Code":
                            newLineItemInv[lineItemColumn] = lineItemData
                            
                            product = products.read(lineItem["Product Code"])
                            if product[0]['Is Error']:
                                newLineItemInv["Product Name"] = ""
                            else:
                                newLineItemInv["Product Name"] = product[1]["Name"]
                        else:
                            newLineItemInv[lineItemColumn] = lineItemData
                    newLineItemList.append(newLineItemInv)
                newValue[invoiceColumn] = newLineItemList
            else:
                newValue[invoiceColumn] = invoiceData
        result[invoiceNo] = newValue
    #print (result)
    printDictInCSVFormat(result, ('Invoice No',), ('Date', 'Customer Code','Due Date','Total','VAT','Amount Due','Items List'))
    return result #send result for caller program to use    

# functions about Receipt
def create_receipt(receipts, receiptNo, receiptDate, customerCode, customerName, PaymentMethod, 
    PaymentReference, Remarks, receiptLineTuplesList) :
    result = receipts.create(receiptNo, receiptDate, customerCode, customerName, PaymentMethod, 
    PaymentReference, Remarks, receiptLineTuplesList)

    if result['Is Error']: #if error
        print(result['Error Message'])
    else:
        print('Receipt Create Success.')
    return result #send result for caller program to use

def read_receipt(receipts, receiptNo) :
    result = receipts.read(receiptNo) #returns tuple of (error dict, data dict)

    if result[0]['Is Error']: #in case error
        print(result[0]['Error Message'])
    else:
        print(result[1])
    return result #send result for caller program to use

def update_receipt(receipts, receiptNo, newreceiptDate, newcustomerCode, newcustomerName, newPaymentMethod, 
    newPaymentReference, newRemarks, newreceiptLineTuplesList) :
    result = receipts.update(receiptNo, newreceiptDate, newcustomerCode, newcustomerName, newPaymentMethod, 
    newPaymentReference, newRemarks, newreceiptLineTuplesList)

    if result['Is Error']: #if error
        print(result['Error Message'])
    else:
        print('Receipt Update Success.')
    return result #send result for caller program to use

def delete_receipt(receipts, receiptNo) :
    result = receipts.delete(receiptNo)

    if result['Is Error']: #if error
        print(result['Error Message'])
    else:
        print('Receipt Delete Success.')
    return result #send result for caller program to use

def report_list_receipt(receipt):
    result = receipt.dump()
    print(result)
    return result

def update_receipt_line(receipts, receiptNo, InvoiceNo, AmountPaidHere) :
    result = receipts.update_receipt_line(receiptNo, InvoiceNo, AmountPaidHere)
    
    if result['Is Error']: #if error
        print(result['Error Message'])
    else:
        print('Receipt Line Item Update Success.')
    return result #send result for caller program to use

def delete_receipt_line(receipts, receiptNo, InvoiceNo) :
    result = receipts.delete_receipt_line(receiptNo, InvoiceNo)

    if result['Is Error']: #if error
        print(result['Error Message'])
    else:
        print('Receipt Line Item Delete Success.')
    return result #send result for caller program to use

def report_list_all_receipts(receipts, invoices, customers):
    allReceipt = receipts.dump()
    # re-format result by add Customer Name in object and Product Name in line item
    result = {}
    # allReceipt = receipts.dump() = {receiptNo : receiptDetail}
    # allReceipt.items() = [(receiptNo, receiptDetail)]
    # receiptDetail is a dict in dict
    for receiptNo, receiptDetail in allReceipt.items():
        newValue = {}
        # receiptDetail = {receiptColumn : receiptData}
        # receiptDetail.items() = [(receiptColumn, receiptData)]
        for receiptColumn, receiptData in receiptDetail.items():
            if receiptColumn == "Customer Code":
                newValue[receiptColumn] = receiptData
                customer = customers.read(receiptDetail["Customer Code"])
                # if can not find 
                if customer[0]['Is Error']:
                    newValue["Customer Name"] = ""
                else:
                    newValue["Customer Name"] = customer[1]["Name"]
            elif receiptColumn == "Sales Invoices":
                newLineItemList = []
                for lineItem in receiptDetail['Sales Invoices']:
                    newLineItemInv = {}
                    for lineItemColumn, lineItemData in lineItem.items():
                        if lineItemColumn == "Invoice No":
                            newLineItemInv[lineItemColumn] = lineItemData

                            invoice = invoices.read(lineItem["Invoice No"])
                            if invoice[0]['Is Error']:
                                newLineItemInv["Date"] = ""
                                newLineItemInv["Customer Code"] = ""
                                newLineItemInv["Due Date"] = ""
                                newLineItemInv["Total"] = ""
                                newLineItemInv["VAT"] = ""
                                newLineItemInv["Amount Due"] = ""
                            else:
                                newLineItemInv["Date"] = invoice[1]["Date"]
                                newLineItemInv["Customer Code"] = invoice[1]["Customer Code"]
                                newLineItemInv["Due Date"] = invoice[1]["Due Date"]
                                newLineItemInv["Total"] = invoice[1]["Total"]
                                newLineItemInv["VAT"] = invoice[1]["VAT"]
                                newLineItemInv["Amount Due"] = invoice[1]["Amount Due"]
                        else:
                            newLineItemInv[lineItemColumn] = lineItemData
                    newLineItemList.append(newLineItemInv)
                newValue[receiptColumn] = newLineItemList
            else:
                newValue[receiptColumn] = receiptData
        result[receiptNo] = newValue
    #print (result)
    printDictInCSVFormat(result, ('Receipt No',), ('Customer Name', 'Sales Invoices'))
    return result

def report_unpaid_invoices(invoices, customers, receipts):
    allReceipt = receipts.dump()
    allInvoice = invoices.dump()
    result = {}
    for invoiceColumn, invoiceData in allInvoice.items():
        newLineItemInv = {}
        invoice = invoices.read(invoiceColumn)
        for line in invoiceData.keys():
            if line == "Date" :
                newLineItemInv["Invoice date"] = invoice[1]["Date"]
            if line == "Customer Code" :
                Customer_Name = customers.read(invoice[1]["Customer Code"])
                newLineItemInv["Customer name"] = Customer_Name[1]["Name"]
            if line == "Amount Due" :
                newLineItemInv["Invoice Amount Due"] = invoice[1]["Amount Due"]
            
            newLineItemInv["Invoice Amount Received"] = 0
            newLineItemInv["Invoice Amount Not Paid"] = 0

        result[invoiceColumn] = newLineItemInv            
   
    newLineItemRct = {}
    for receiptColumn, receiptData in allReceipt.items():
        for receiptKey in receiptData.keys():
            if receiptKey == 'Sales Invoices':
                for lineItem in receiptData['Sales Invoices']:
                    for lineItemColumn, lineItemData in lineItem.items():
                        if lineItemColumn == "Invoice No" :
                            invoiceNo = lineItemData  
                        if lineItemColumn == "Amount Paid Here":
                            # AmountPaidHere is amount of money that already paid
                            AmountPaidHere = lineItemData
                    if invoiceNo in newLineItemRct:
                        newLineItemRct[invoiceNo] = newLineItemRct[invoiceNo]+AmountPaidHere
                    else:
                        newLineItemRct[invoiceNo] = AmountPaidHere

    TotalInvAmtNotPaid = 0
    for Inv,Invdata in result.items() :
        for Rct in newLineItemRct.keys() :
            if Inv == Rct :
                Invdata["Invoice Amount Received"] += newLineItemRct[Rct]
                InvAmtNotPaid = Invdata["Invoice Amount Due"] - Invdata["Invoice Amount Received"]
                Invdata["Invoice Amount Not Paid"] = InvAmtNotPaid
                TotalInvAmtNotPaid += InvAmtNotPaid
    
    printDictData(result)
    print("Total Invoice Amount Not Paid ",TotalInvAmtNotPaid)
    return result, TotalInvAmtNotPaid

def report_products_sold(invoices, products, dateStart, dateEnd):
    # Will return 2 dictionaries: 
    # 1) a dictionary as list of in products sold in the given date range in tabular format of: Product Code, Product Name, Total Quantity Sold, Total Value Sold. Here, (product code) will be unique. 
    # And 2) a second dictionary of the footer will also be returned containing: t the end also show the sum of Total Value Sold.  
    allInvoice = invoices.dump()
    result = {}
    result2 = {}
    sumTotalValueSold = 0
    for key, value in allInvoice.items():
        if (dateStringInDateRange(value['Date'], dateStart, dateEnd)):
            for lineItem in value['Items List']:
                primaryKey = lineItem['Product Code']
                if primaryKey in result:
                    result[primaryKey]['Total Quantity Sold'] += lineItem['Quantity']
                    result[primaryKey]['Total Value Sold'] += lineItem['Extended Price']
                else:
                    product = products.read(lineItem["Product Code"])
                    if product[0]['Is Error']:
                        productName = ""
                    else:
                        productName = product[1]["Name"]
                    result[primaryKey] = {'Product Code':lineItem['Product Code'], 'Product Name':productName,'Total Quantity Sold':lineItem['Quantity'],'Total Value Sold':lineItem['Extended Price']}
                sumTotalValueSold += lineItem['Extended Price']

    result2['Sum of'] = {'Total Value Sold':sumTotalValueSold}
    printDictInCSVFormat(result, (None), ('Product Code','Product Name', 'Total Quantity Sold', 'Total Value Sold'))
    printDictInCSVFormat(result2, (None), ('Total Value Sold',))
    return result.values(), result2

def report_customer_products_sold_list(invoices, products, customers, dateStart, dateEnd):
    # Will return 2 dictionaries: 
    # 1) a dictionary as list of customers and list the products sold to them in the given date range in this format:  Customer Code, Customer Name, Product Code,  Product Name, Invoice No, Invoice Date, Quantity Sold, Value Sold. Here, (customer code, product code, invoice no) will be unique.  
    # And 2) a second footer dictionary showing:  At the end also show the sum of Quantity Sold and sum of Value Sold.
    allInvoice = invoices.dump()
    result = {}
    result2 = {}
    sumTotalQuantitySold = 0
    sumTotalValueSold = 0
    for key, value in allInvoice.items():
        invoiceNo = key
        if (dateStringInDateRange(value['Date'], dateStart, dateEnd)):
            for lineItem in value['Items List']:
                primaryKey = value['Customer Code'] + lineItem['Product Code'] + invoiceNo
                if primaryKey in result:
                    result[primaryKey]['Quantity Sold'] += lineItem['Quantity']
                    result[primaryKey]['Value Sold'] += lineItem['Extended Price']
                else:
                    product = products.read(lineItem["Product Code"])
                    if product[0]['Is Error']:
                        productName = ""
                    else:
                        productName = product[1]["Name"]

                    customer = customers.read(value['Customer Code'])
                    if customer[0]['Is Error']:
                        customerName = ""
                    else:
                        customerName = customer[1]["Name"]
                    result[primaryKey] = {'Customer Code':value['Customer Code'],'Customer Name':customerName,'Product Code':lineItem['Product Code'], 'Product Name':productName,'Invoice No':invoiceNo,'Invoice Date':value['Date'],'Quantity Sold':lineItem['Quantity'],'Value Sold':lineItem['Extended Price']}
                sumTotalQuantitySold += lineItem['Quantity']
                sumTotalValueSold += lineItem['Extended Price']

    result2['Sum of'] = {'Quantity Sold':sumTotalQuantitySold,'Value Sold':sumTotalValueSold}
    printDictInCSVFormat(result, (None), ('Customer Code','Customer Name', 'Product Code', 'Product Name', 'Invoice No', 'Invoice Date', 'Quantity Sold', 'Value Sold'))
    printDictInCSVFormat(result2, (None), ('Quantity Sold','Value Sold'))
    return result.values(), result2

def report_customer_products_sold_total(invoices, products, customers, dateStart, dateEnd):
    # Will return 2 dictionaries: 
    # 1) a dictionary as list customers and the total number and value of products sold to them in the given date range in this format:  Customer Code, Customer Name, Product Code,  Product Name, Total Quantity Sold, Total Value Sold. Here (customer code, product code) will be unique.
    # And 2) a second footer dictionary showing: t the end also show the sum of Total Quantity Sold, sum of Total Value Sold.
    allInvoice = invoices.dump()
    result = {}
    result2 = {}
    sumTotalQuantitySold = 0
    sumTotalValueSold = 0
    for key, value in allInvoice.items():
        invoiceNo = key
        if (dateStringInDateRange(value['Date'], dateStart, dateEnd)):
            for lineItem in value['Items List']:
                primaryKey = value['Customer Code'] + lineItem['Product Code']
                if primaryKey in result:
                    result[primaryKey]['Total Quantity Sold'] += lineItem['Quantity']
                    result[primaryKey]['Total Value Sold'] += lineItem['Extended Price']
                else:
                    product = products.read(lineItem["Product Code"])
                    if product[0]['Is Error']:
                        productName = ""
                    else:
                        productName = product[1]["Name"]

                    customer = customers.read(value['Customer Code'])
                    if customer[0]['Is Error']:
                        customerName = ""
                    else:
                        customerName = customer[1]["Name"]
                    result[primaryKey] = {'Customer Code':value['Customer Code'],'Customer Name':customerName,'Product Code':lineItem['Product Code'], 'Product Name':productName,'Total Quantity Sold':lineItem['Quantity'],'Total Value Sold':lineItem['Extended Price']}
                sumTotalQuantitySold += lineItem['Quantity']
                sumTotalValueSold += lineItem['Extended Price']

    result2['Sum of'] = {'Total Quantity Sold':sumTotalQuantitySold,'Total Value Sold':sumTotalValueSold}
    printDictInCSVFormat(result, (None), ('Customer Code','Customer Name', 'Product Code', 'Product Name', 'Total Quantity Sold', 'Total Value Sold'))
    printDictInCSVFormat(result2, (None), ('Total Quantity Sold','Total Value Sold'))
    return result.values(), result2
