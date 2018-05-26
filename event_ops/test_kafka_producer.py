from producer import EventPublisher
import pytest, time
k_obj = EventPublisher()

def test_send_message():
    while True:
        k_obj.publish('orders',{'test':'val'})
