class Receipt:
    def __init__(self):
        self.dict = {}
    
    def __updateLineItem (self, receiptLineTuplesList):
        totalreceived = 0
        receiptLineItemList = []
        for lineItem in receiptLineTuplesList:
            receiptLineItem = {}
            receiptLineItem["Invoice No"] = lineItem["Invoice No"]
            receiptLineItem["Amount Paid Here"] = lineItem["Amount Paid Here"]
            
            totalreceived += receiptLineItem["Amount Paid Here"]
            receiptLineItemList.append(receiptLineItem)

        return receiptLineItemList, totalreceived

    def create(self, receiptNo, receiptDate, customerCode, customerName, PaymentMethod, 
    PaymentReference, Remarks, receiptLineTuplesList):

        if receiptNo in self.dict:
            return {'Is Error': True, 'Error Message': "Receipt No '{}' already exists. Cannot Create. ".format(receiptNo)}

        else:
            receiptLineItemList, totalreceived = self.__updateLineItem(receiptLineTuplesList)
            
            self.dict[receiptNo] = {"Date" : receiptDate,"Customer Code" : customerCode,
            "Customer Name" : customerName, "Payment Method" : PaymentMethod, "Total Received" : totalreceived,
            "Payment Reference" : PaymentReference,"Sales Invoices" : receiptLineItemList, "Remarks" : Remarks}

        return {'Is Error': False, 'Error Message': ""}

    def read(self, receiptNo):
 
        if receiptNo in self.dict:
            retReceipt = self.dict[receiptNo]
        else:
            return ({'Is Error': True, 'Error Message': "Receipt No '{}' not found. Cannot Read.".format(receiptNo)},{})

        return ({'Is Error': False, 'Error Message': ""}, retReceipt)

    def update(self, receiptNo, newreceiptDate, newcustomerCode, newcustomerName, newPaymentMethod, 
    newPaymentReference, newRemarks, newreceiptLineTuplesList):
        
        if receiptNo in self.dict:
            self.dict[receiptNo]["Date"] = newreceiptDate
            self.dict[receiptNo]["Customer Code"] = newcustomerCode
            self.dict[receiptNo]["Customer Name"] = newcustomerName
            self.dict[receiptNo]["Payment Method"] = newPaymentMethod
            self.dict[receiptNo]["Payment Reference"] = newPaymentReference
            self.dict[receiptNo]["Remarks"] = newRemarks

            receiptLineItemList, totalreceived, = self.__updateLineItem(newreceiptLineTuplesList)
            
            self.dict[receiptNo]["Total Received"] = totalreceived
            self.dict[receiptNo]["Sales Invoices"] = receiptLineItemList
        else:
            return {'Is Error': True, 'Error Message': "Receipt No '{}' not found. Cannot Update.".format(receiptNo)}

        return {'Is Error': False, 'Error Message': ""}

    def delete(self, receiptNo):

        if receiptNo in self.dict:
            del self.dict[receiptNo]

        else:
            return {'Is Error': True, 'Error Message': "Receipt No '{}' not found. Cannot Delete".format(receiptNo)}
        return {'Is Error': False, 'Error Message': ""}

    def dump(self):

        return (self.dict)

    def update_receipt_line(self, receiptNo, InvoiceNo, AmountPaidHere):

        if receiptNo in self.dict:
            receivedtotal = 0
            newReceiptLineTuplesList = []
            bUpdated = False
            for lineItem in self.dict[receiptNo]["Sales Invoices"]:
                receiptLineItem = {}
                if lineItem["Invoice No"] == InvoiceNo :
                    receiptLineItem["Invoice No"] = InvoiceNo
                    receiptLineItem["Amount Paid Here"] = AmountPaidHere

                    newReceiptLineTuplesList.append(receiptLineItem)
                    bUpdated = True
                else:
                    newReceiptLineTuplesList.append(lineItem)
            
            if bUpdated:
                receiptLineItemList, receivedtotal, = self.__updateLineItem(newReceiptLineTuplesList)

                self.dict[receiptNo]["Total Received"] = receivedtotal
                self.dict[receiptNo]["Sales Invoices"] = receiptLineItemList
            else:
                return {'Is Error': True, 
                'Error Message': "Invoice No '{}' not found in Receipt No '{}'. Cannot Update.".format(InvoiceNo, receiptNo)}
        else:
            return {'Is Error': True, 'Error Message': "Receipt No '{}' not found. Cannot Update.".format(receiptNo)}
            
        return {'Is Error': False, 'Error Message': ""}

    def delete_receipt_line(self, receiptNo, InvoiceNo):

        if receiptNo in self.dict:
            receivedtotal = 0
            receiptLineItemList = []
            bDeleted = False
            for lineItem in self.dict[receiptNo]["Sales Invoices"]:
                #receiptLineItem = {}
                if lineItem["Invoice No"] == InvoiceNo :
                    bDeleted = True
                else:
                    receiptLineItemList.append(lineItem)
            
            if bDeleted:
                receiptLineItemList, receivedtotal = self.__updateLineItem(receiptLineItemList)

                self.dict[receiptNo]["Total Received"] = receivedtotal
                self.dict[receiptNo]["Sales Invoices"] = receiptLineItemList
            else:
                return {'Is Error': True, 
                'Error Message': "Invoice No '{}' not found in Receipt No '{}'. Cannot Delete.".format(InvoiceNo, receiptNo)}
        else:
            return {'Is Error': True, 'Error Message': "Receipt No '{}' not found. Cannot Delete.".format(receiptNo)}

        return {'Is Error': False, 'Error Message': ""}
  