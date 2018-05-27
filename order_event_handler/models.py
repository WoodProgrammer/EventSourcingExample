
from pymongo import MongoClient
from bson import ObjectId

import json

class OrderEventModel(dict):

    __getattr__ = dict.get
    __delattr__ = dict.__delitem__
    __setattr__ = dict.__setitem__

    collection = MongoClient()["order_test_db"]["order_test_col"]
    log_collection = MongoClient()["order_test_db"]["order_test_log"]



    def change_order(self, order_id, state):
        self.collection.update({'order_id':order_id }, {'$set': {'STATE':'{}'.format(state)}} )


    def find_with_id(self,order_id):
        return self.collection.find({'order_id':id})
