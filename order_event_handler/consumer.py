from kafka import KafkaConsumer
from publisher import EventPublisher
from models import OrderEventModel
import json

consumer = KafkaConsumer('order', group_id='view', bootstrap_servers=['192.168.99.100:9092'] )
publisher = EventPublisher()
model_handler = OrderEventModel()

for msg in consumer:
    tmp_json = json.loads(msg.value)
    print(tmp_json)
    try: ### foolish bug cause of me. will be fix ### FIX 1
    ####SHIPPING OPERATION WILL ADDING HERE (UPDATE )
        if tmp_json['state'] == 'VALIDATED' :## model changing

            order_id = tmp_json['order_id']
            model_handler.change_order(order_id=order_id, state='SHIPPED')
            print("PAYMENT STATE CHANGED!")
            publisher.publish(data={'stock_id':tmp_json['stock_id'], 'change_count':tmp_json['count']},topic_name='stock')
    except:
        if tmp_json['payment_state'] == 'VALIDATED' :## model changing

            order_id = tmp_json['order_id']
            model_handler.change_order(order_id=order_id, state='SHIPPED')
            print("PAYMENT STATE CHANGED!")
            publisher.publish(data={'stock_id':tmp_json['stock_id'], 'change_count':tmp_json['count']},topic_name='stock')
