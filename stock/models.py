
from pymongo import MongoClient
from bson import ObjectId
from producer import EventPublisher

import json
event_handler = EventPublisher()

class Stock(dict):

    __getattr__ = dict.get
    __delattr__ = dict.__delitem__
    __setattr__ = dict.__setitem__

    collection = MongoClient()["stock_test_db"]["stock_test_col"]
    log_collection = MongoClient()["stock_test_db"]["stock_test_log"]

    def save(self):
        if not self._id:
            self.collection.insert(self)

        else:
            self.collection.update(
                { "_id": ObjectId(self._id) }, self)

    def all_stocks(self):
        stock_arr = []
        for stock in self.collection.find():
            try:
                stock_arr.append({'stock_id' : stock['stock_id'], 'stock_id' : stock['stock_id'], 'count':stock['count'], 'price': stock['price'],'state': stock['state']})
            except:##key errr
                stock_arr.append({'stock_id' : stock['stock_id'], 'stock_id' : stock['stock_id'], 'count':stock['count'], 'price': stock['price']})

        return stock_arr


    def get_stock(self, stock_id):
        stock_data = self.collection.find_one({"stock_id": stock_id})
        if stock_data is None:
            return {}
        else:
            return {"stock_id":stock_data['stock_id'], "stock_id": stock_data["stock_id"],"count": stock_data["count"]}


    def  delete_stock(self, stock_id):
        try:
            self.collection.remove({"stock_id":stock_id})
            return 1
        except Exception as exp:

            self.log_collection.insert({"log_message":str(exp)})
            return 0

    def set_stock(self, stock_payload):
        
        print(stock_payload)
        event_handler.publish(data=stock_payload)
        self.collection.insert(stock_payload)
