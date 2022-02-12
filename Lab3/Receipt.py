from DBHelper import DBHelper
from helper_functions import *
#This file made by JapPapin if u copy this pls delete this line

class Receipt :
    def __init__(self) :
        self.db = DBHelper()
    def __updateTotalReceived(self, receiptNo) :
        sql = ("UPDATE receipt SET"
              " total_received = line_item.new_total_received "
              " FROM (SELECT receipt_no, SUM(amount_paid_here) as new_total_received FROM receipt_line_item GROUP BY receipt_no) line_item"
              " WHERE receipt.receipt_no = line_item.receipt_no"
              " AND receipt.receipt_no = '{}'".format(receiptNo))
        self.db.execute(sql)

    def __updateLineItem(self, receiptNo, receipLineTuplesList) :
        self.db.execute ("DELETE FROM receipt_line_item WHERE receipt_no = '{}'".format(receiptNo))
        for lineItem in receipLineTuplesList :
            sql = "INSERT INTO receipt_line_item (receipt_no, invoice_no, amount_paid_here) VALUES ('{}', '{}', {})"
            self.db.execute (sql.format(receiptNo, lineItem["Invoice No"], lineItem["Amount Paid Here"]))
        self.__updateTotalReceived(receiptNo)

    def create(self, receiptNo, receiptDate, customerCode, paymentMethod, paymentReference, remarks, receipLineTuplesList) :
        data, columns = self.db.fetch ("SELECT * FROM receipt WHERE receipt_no = '{}'".format(receiptNo))
        if len(data) > 0 :
            return {'Is Error': True, 'Error Message': "Receipt No '{}' already exists. Cannot Create. ".format(receiptNo)}
        else :
            sql = "INSERT INTO receipt (receipt_no, date, customer_code, payment_method, payment_reference, remarks) VALUES ('{}', {}, '{}', '{}', '{}','{}')"
            self.db.execute (sql.format(receiptNo, receiptDate, customerCode, paymentMethod, paymentReference, remarks)) 
            self.__updateLineItem(receiptNo, receipLineTuplesList)           
        return {'Is Error': False, 'Error Message': ""}

    def read(self, receiptNo) :
        data, columns = self.db.fetch ("SELECT * FROM receipt WHERE receipt_no = '{}'".format(receiptNo))  
        if len(data) > 0:
            retReceipt = row_as_dict(data, columns)
        else:
            return {'Is Error': True, 'Error Message': "Receipt No '{}' not found. Cannot Read.".format(receiptNo)},{}

        return {'Is Error': False, 'Error Message': ""},retReceipt

    def update(self, receiptNo, newReceiptDate, newCustomerCode, newPaymentMethod, newPaymentReference, newRemarks, newReceiptLineTupleList) :
        data, columns = self.db.fetch ("SELECT * FROM receipt WHERE receipt_no = '{}'".format(receiptNo))  
        if len(data) > 0:
            self.db.execute ("UPDATE receipt SET date = {}, customer_code = '{}', payment_method = '{}', payment_reference = '{}', remarks = '{}' WHERE receipt_no = '{}'"
            .format(newReceiptDate, newCustomerCode, newPaymentMethod, newPaymentReference, newRemarks, receiptNo))
            self.__updateLineItem(receiptNo, newReceiptLineTupleList)
        else:
            return {'Is Error': True, 'Error Message': "Receipt No '{}' not found. Cannot Read.".format(receiptNo)}

        return {'Is Error': False, 'Error Message': ""}

    def delete(self, receiptNo) :
        data, columns = self.db.fetch ("SELECT * FROM receipt WHERE receipt_no = '{}'".format(receiptNo))  
        if len(data) > 0:
            self.db.execute ("DELETE FROM receipt_line_item WHERE receipt_no = '{}'".format(receiptNo))
            self.db.execute ("DELETE FROM receipt WHERE receipt_no = '{}'".format(receiptNo))
        else:
            return {'Is Error': True, 'Error Message': "Receipt No '{}' not found. Cannot Read.".format(receiptNo)}

        return {'Is Error': False, 'Error Message': ""}

    def dump(self) :
        db = DBHelper()
        sql = """ SELECT CONCAT(r.receipt_no, i.invoice_no) as "Receipt No : Invoice No"
                , r.receipt_no as "Receipt No", r.date as "Date", r.customer_code as "Customer Code" 
                , c.name as "Customer Name", r.payment_method as "Payment Method", r.payment_reference as "Payment Reference" 
                , r.total_received as "Total Received", r.remarks as "Remarks", i.invoice_no as "Invoice No"
                , i.date as "Invoice Date", i.amount_due as "Invoice Full Amount", rli.amount_paid_here as"Amount Paid Here"   
                FROM receipt r JOIN customer c ON r.customer_code = c.customer_code 
                JOIN receipt_line_item rli ON r.receipt_no = rli.receipt_no 
                JOIN invoice i ON rli.invoice_no = i.invoice_no """
        data, columns = db.fetch (sql)
        result = row_as_dict(data, columns)
        return result

    def update_receipt_line(self, receiptNo, invoiceNo, newAmountPaidHere) :
        data, columns = self.db.fetch ("SELECT * FROM receipt_line_item WHERE receipt_no = '{}' AND invoice_no = '{}'".format(receiptNo, invoiceNo))
        if len(data) > 0 :
            self.db.execute ("UPDATE receipt_line_item SET amount_paid_here = {} WHERE receipt_no = '{}' AND invoice_no = '{}'"
            .format(newAmountPaidHere, receiptNo, invoiceNo))
            self.__updateTotalReceived(receiptNo)
        else:
            return {'Is Error': True, 'Error Message': "Invoice No '{}' not found in Receipt No '{}'. Cannot Update.".format(invoiceNo, receiptNo)}

        return {'Is Error': False, 'Error Message': ""} 

    def delete_receipt_line(self, receiptNo, invoiceNo) :
        data, columns = self.db.fetch ("SELECT * FROM receipt_line_item WHERE receipt_no = '{}' AND invoice_no = '{}'".format(receiptNo, invoiceNo))
        if len(data) > 0 :
            self.db.execute ("DELETE FROM receipt_line_item WHERE receipt_no = '{}' AND invoice_no = '{}'".format(receiptNo, invoiceNo))
            self.__updateTotalReceived(receiptNo)
        else:
            return {'Is Error': True, 'Error Message': "Invoice No '{}' not found in Receipt No '{}'. Cannot Update.".format(invoiceNo, receiptNo)}

        return {'Is Error': False, 'Error Message': ""}                                       
