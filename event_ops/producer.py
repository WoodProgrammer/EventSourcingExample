import json
from bson import json_util

from kafka import KafkaProducer

class EventPublisher:

    def __init__(self):

        self.producer = KafkaProducer(bootstrap_servers='192.168.99.100:9092')

    def publish(self, topic_name, data):

        self.producer.send(topic_name, json.dumps(data, indent=4, default=json_util.default).encode('utf-8'))
