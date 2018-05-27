from models import OrderEventModel
obj = OrderEventModel()

def test_update():
    obj.change_order(order_id=1, state="SHIPPED")

def test_validate_update():

    data = obj.find_with_id(order_id=1)
    print(data[0])
