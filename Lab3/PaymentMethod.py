from DBHelper import DBHelper
from helper_functions import *

class PaymentMethod:
    def __init__(self) :
        self.db = DBHelper()   
    def create(self, code, name) :
        data, columns = self.db.fetch ("SELECT * FROM payment_method WHERE code = '{}' ".format(code))
        if len(data) > 0:
            return {'Is Error': True, 'Error Message': "payment_method code '{}' already exists. Cannot Create. ".format(code)}
        else:
            self.db.execute ("INSERT INTO payment_method VALUES ('{}' ,'{}')".format(code,name))
        return {'Is Error': False, 'Error Message': ""}        
    def read(self, code) :
        data, columns = self.db.fetch ("SELECT * FROM payment_method WHERE code = '{}'".format(code))
        if len(data) > 0 :
            retpayment_method = row_as_dict(data, columns) 
        else:
            return ({'Is Error': True, 'Error Message': "payment_method Code '{}' not found. Cannot Read".format(code)},{})
        return ({'Is Error': False, 'Error Message': ""},retpayment_method)      
    def update(self, code, newName) :
        data, columns = self.db.fetch ("SELECT * FROM payment_method WHERE code = '{}'".format(code))
        if len(data) > 0 :
            self.db.execute ("UPDATE payment_method SET name = '{}' WHERE code = '{}'".format(newName, code))
        else:
            return {'Is Error': True, 'Error Message': "payment_method Code '{}' not found. Cannot Update".format(code)}
        return {'Is Error': False, 'Error Message': ""}            
    def delete(self, code) :
        data, columns = self.db.fetch ("SELECT * FROM payment_method WHERE code = '{}'".format(code))
        if len(data) > 0 :
            self.db.execute ("DELETE FROM payment_method WHERE code = '{}'".format(code))
        else:
            return {'Is Error': True, 'Error Message': "payment_method Code '{}' not found. Cannot Delete".format(code)}
        return {'Is Error': False, 'Error Message': ""}
    def dump(self) :
        data, columns = self.db.fetch ('SELECT code as "Code", name as "Name" FROM payment_method ')
        return row_as_dict(data, columns)