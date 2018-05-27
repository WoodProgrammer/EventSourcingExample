from flask import Flask, jsonify, request
from models import Stock

app = Flask(__name__)
order_obj = Orders()



@app.route("/order")
def order():
    data = order_obj.all_orders()
    return jsonify(data)

@app.route("/create_order", methods=["POST"])
def create_order():
    order_payload =  request.json
    order_obj.set_order(order_payload= order_payload)

    return jsonify({"order_id":order_payload["order_id"],"stock_id":order_payload["stock_id"],"count":order_payload["count"],"price":order_payload["price"]})


@app.route("/delete_order", methods=["DELETE"])
def delete_order():
    order_payload =  request.json
    try:
        order_obj.delete_order(order_id= order_payload["order_id"])
        return jsonify({'status':'OK'}), 200
    except:
        return jsonify({'status':'ERROR'}), 500


if __name__ == "__main__":
    app.run(debug=True)
