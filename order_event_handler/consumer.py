from kafka import KafkaConsumer
from publisher import EventPublisher
import json

consumer = KafkaConsumer('order', group_id='view', bootstrap_servers=['192.168.99.100:9092'] )
publisher = EventPublisher()

for msg in consumer:
    tmp_json = json.loads(msg.value)
    if tmp_json['state'] == 'SHIPPED':
        stock_count = tmp_json['count']

        publisher.publish(data={'stock_id':tmp_json['stock_id'], 'change_count':stock_count},topic_name='stock', count=stock_count)
