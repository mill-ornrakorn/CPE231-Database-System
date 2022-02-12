from helper_functions import *
from API import *
from Customer import *
from Product import *
from Invoice import *
from Receipt import *

def main() :    
    try:
        #Create products obj 
        products = Product()
        create_product(products, "HD01", "Seagate HDD 80 GB", "PCS")
        create_product(products, "HD02", "IBM HDD 60 GB", "PCS")
        create_product(products, "INT01", "Intle Pentium IV 3.6 GHz", "PCS")
        report_list_products(products)
        waitKeyPress("Above are results for creating 3 products.")
        print("\n")

        #Create customers obj 
        customers = Customer()
        create_customer(customers, "Sam", "Sam Co., Ltd.", "122 Bangkok", 500000, "Thailand")
        create_customer(customers, "CP", "Charoen Pokaphan", "14 Sukhumvit, Bangkok", 2000000, "Thailand")
        report_list_all_customers(customers)
        waitKeyPress("Above are results for creating 2 customers.") 
        print("\n")

        #Create invoices obj 
        invoices = Invoice()
        create_invoice(invoices, "INT100/20", "2020-01-02", "Sam", None, 
        [{"Product Code":"HD01", "Quantity":2, "Unit Price":3000},
        {"Product Code":"HD02", "Quantity":1, "Unit Price":2000}])
        create_invoice(invoices, "INT101/20", "2020-01-04", "CP", None, 
        [{"Product Code":"HD02","Quantity":1,"Unit Price":2000}])
        report_list_all_invoices(invoices, customers, products)
        waitKeyPress("Above are results for creating 2 invoices and line item.")
        print("\n")
        
        #Create receipts obj
        receipts = Receipt()
        create_receipt(receipts,"RCT1002/20","2020-02-05","Sam","Sam Co., Ltd.",
        "Credit Card","Master Card, Citibank","Partially paid on INT101/20",
        [{'Invoice No':'INT100/20', 'Amount Paid Here':8560.00},
        {'Invoice No':'INT101/20', 'Amount Paid Here':1440.00}])

        #if the receipt has already exists, the error message will be shown
        create_receipt(receipts,"RCT1002/20","2020-02-06","Sam","Sam Co., Ltd.",
        "Credit Card","Master Card, Citibank","Partially paid on INT101/20",
        [{'Invoice No':'INT100/20', 'Amount Paid Here':8560.00},
        {'Invoice No':'INT101/20', 'Amount Paid Here':1440.00}])
        report_list_all_receipts(receipts, invoices, customers)    
        waitKeyPress("Above are results for creating receipt and line item.")
        print("\n")
        
        #Read Receipts
        read_receipt(receipts,"RCT1002/20")
        
        #if the input receipt No was not exist, the error message will be shown
        read_receipt(receipts,"RCT1003/20")        
        waitKeyPress("Above are results for reading receipt No. RCT1002/20.")
        print("\n")
        
        #Update Receipts
        #Change Receipt No. RCT1002/20
        #Change Date 2020-02-05 to 2020-02-10
        update_receipt(receipts,"RCT1002/20","2020-02-10","Sam","Sam Co., Ltd.",
        "Credit Card","Master Card, Citibank","Partially paid on INT101/20",
        [{'Invoice No':'INT100/20', 'Amount Paid Here':8560.00},
        {'Invoice No':'INT101/20', 'Amount Paid Here':1440.00}])
        #if the input receipt No was not exist, the error message will be shown
        update_receipt(receipts,"RCT1003/20","2020-02-10","Sam","Sam Co., Ltd.",
        "Credit Card","Master Card, Citibank","Partially paid on INT101/20",
        [{'Invoice No':'INT100/20', 'Amount Paid Here':8560.00},
        {'Invoice No':'INT101/20', 'Amount Paid Here':1440.00}])        
        report_list_all_receipts(receipts, invoices, customers)
        waitKeyPress("Above are results for updating receipt No. RCT1002/20. and line item")
        print("\n")
        #Change back 
        update_receipt(receipts,"RCT1002/20","2020-02-05","Sam","Sam Co., Ltd.",
        "Credit Card","Master Card, Citibank","Partially paid on INT101/20",
        [{'Invoice No':'INT100/20', 'Amount Paid Here':8560.00},
        {'Invoice No':'INT101/20', 'Amount Paid Here':1440.00}])

        #Delete Receipts
        delete_receipt(receipts, "RCT1002/20")

        #if the input receipt No was not exist, the error message will be shown 
        delete_receipt(receipts, "RCT1003/20")       
        report_list_all_receipts(receipts, invoices, customers)
        waitKeyPress("Above are results for deleting receipt No. RCT1002/20.")
        print("\n")
                
        #Re-Create 
        create_receipt(receipts,"RCT1002/20","2020-02-05","Sam","Sam Co., Ltd.",
        "Credit Card","Master Card, Citibank","Partially paid on INT101/20",
        [{'Invoice No':'INT100/20', 'Amount Paid Here':8560.00},
        {'Invoice No':'INT101/20', 'Amount Paid Here':1440.00}])

        #Update receipt line
        #Change Receipt No. RCT1002/20 Invoice No. INT101/20
        #Change Amount Paid Here 8560.00 to 8000
        update_receipt_line(receipts, "RCT1002/20", "INT101/20", 8000.00)    

        #if the input receipt No was not exist, the error message will be shown
        update_receipt_line(receipts, "RCT1003/20", "INT101/20", 8000.00)

        #if the input invoice No was not exist, the error message will be shown
        update_receipt_line(receipts, "RCT1002/20", "INT103/20", 8000.00)

        report_list_all_receipts(receipts, invoices, customers)
        waitKeyPress("Above are results for updating receipt No. RCT1002/20 Invoice No. INT100/20.")
        print("\n")
        
        #Re-update
        update_receipt_line(receipts, "RCT1002/20", "INT101/20", 8560.00)    

        #Delete receipt line
        #Delete Receipt No. RCT1002/20 Invoice No. INT100/20
        delete_receipt_line(receipts, "RCT1002/20", "INT100/20")

        #if the input receipt No was not exist, the error message will be shown
        delete_receipt_line(receipts, "RCT1003/20", "INT101/20")

        #if the input invoice No was not exist, the error message will be shown
        delete_receipt_line(receipts, "RCT1002/20", "INT103/20")

        report_list_all_receipts(receipts, invoices, customers)
        waitKeyPress("Above are results for deleting receipt No. RCT1002/20 Invoice No. INT100/20.")
        print("\n")
        
        #Re-create
        delete_receipt(receipts,"RCT1002/20")
        create_receipt(receipts,"RCT1002/20","2020-02-05","Sam","Sam Co., Ltd.",
        "Credit Card","Master Card, Citibank","Partially paid on INT101/20",
        [{'Invoice No':'INT100/20', 'Amount Paid Here':8560.00},
        {'Invoice No':'INT101/20', 'Amount Paid Here':1440.00}])
          
        #Report the unpaid invoices
        report_unpaid_invoices(invoices, customers, receipts)
        waitKeyPress("Above are results of unpaid invoices")

    except: #this traps for unexpected system errors
        print ("Unexpected error:", sys.exc_info()[0])
        raise # this line can be erased. It is here to raise another error so you can see which line to debug.
    else:
        print("Normal Termination.   Goodbye!")
    #main function ends

#this is so that when called externally via a command line, main is executed.
if __name__ == "__main__":
    main()
