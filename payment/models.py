
from pymongo import MongoClient
from bson import ObjectId

import json

class Payment(dict):

    __getattr__ = dict.get
    __delattr__ = dict.__delitem__
    __setattr__ = dict.__setitem__

    collection = MongoClient()["payment_test_db"]["payment_test_col"]
    log_collection = MongoClient()["payment_test_db"]["payment_test_log"]

    def save(self):
        if not self._id:
            self.collection.insert(self)
        else:
            self.collection.update(
                { "_id": ObjectId(self._id) }, self)

    def all_payments(self):
        payment_arr = []
        for payment in self.collection.find():
            payment_arr.append({'payment_id' : payment['payment_id'], 'stock_id' : payment['stock_id'], 'count':payment['count'], 'price': payment['price']})


        return payment_arr


    def get_payment(self, payment_id):
        payment_data = self.collection.find_one({"payment_id": payment_id})
        if payment_data is None:
            return {}
        else:
            return {"payment_id":payment_data['payment_id'], "stock_id": payment_data["stock_id"],"count": payment_data["count"]}


    def  delete_payment(self, payment_id):
        try:
            self.collection.remove({"payment_id":payment_id})
            return 1
        except Exception as exp:

            self.log_collection.insert({"log_message":str(exp)})
            return 0

    def set_payment(self, payment_payload):
        self.collection.insert(payment_payload)
