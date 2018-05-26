
from pymongo import MongoClient
from bson import ObjectId
from producer import EventPublisher

import json
event_handler = EventPublisher()

class Orders(dict):

    __getattr__ = dict.get
    __delattr__ = dict.__delitem__
    __setattr__ = dict.__setitem__

    collection = MongoClient()["order_test_db"]["order_test_col"]
    log_collection = MongoClient()["order_test_db"]["order_test_log"]

    def save(self):
        if not self._id:
            self.collection.insert(self)

        else:
            self.collection.update(
                { "_id": ObjectId(self._id) }, self)

    def all_orders(self):
        order_arr = []
        for order in self.collection.find():
            order_arr.append({'order_id' : order['order_id'], 'stock_id' : order['stock_id'], 'count':order['count'], 'price': order['price']})


        return order_arr


    def get_order(self, order_id):
        order_data = self.collection.find_one({"order_id": order_id})
        if order_data is None:
            return {}
        else:
            return {"order_id":order_data['order_id'], "stock_id": order_data["stock_id"],"count": order_data["count"]}


    def  delete_order(self, order_id):
        try:
            self.collection.remove({"order_id":order_id})
            return 1
        except Exception as exp:

            self.log_collection.insert({"log_message":str(exp)})
            return 0

    def set_order(self, order_payload):
        order_payload['state'] = "CREATED"
        print(order_payload)
        event_handler.publish(data=order_payload)
        self.collection.insert(order_payload)
