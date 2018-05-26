from kafka import KafkaConsumer
import json

consumer = KafkaConsumer('order', group_id='view', bootstrap_servers=['192.168.99.100:9092'] )

for msg in consumer:
    tmp_json = json.loads(msg.value)
    if tmp_json['state'] == 'VERIFIED':
        pass
