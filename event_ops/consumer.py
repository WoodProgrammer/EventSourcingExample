from kafka import KafkaConsumer
import json

consumer = KafkaConsumer('orders', group_id='view', bootstrap_servers=['192.168.99.100:9092'] )

for msg in consumer:
    tmp_json = json.loads(msg.value)
    print(tmp_json['test'])
