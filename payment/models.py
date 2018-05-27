
from pymongo import MongoClient
from bson import ObjectId
from publisher import EventPublisher
import json

event_handler = EventPublisher()

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
            try:
                payment_arr.append({'order_id':payment['order_id'], 'payment_id' : payment['payment_id'], 'stock_id' : payment['stock_id'], 'count':payment['count'], 'price': payment['price'], 'state':payment['state']})
            except:
                payment_arr.append({'order_id':payment['order_id'], 'payment_id' : payment['payment_id'], 'stock_id' : payment['stock_id'], 'count':payment['count'], 'price': payment['price']})


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

    def set_payment(self, payment_payload):## if payment_is okey validate
    ###validate fujnction ()

        payment_payload['payment_state'] = 'VALIDATED'
        event_handler.publish(data=payment_payload)
        self.collection.insert(payment_payload)
