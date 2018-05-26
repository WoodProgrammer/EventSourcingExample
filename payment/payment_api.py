from flask import Flask, jsonify, request
from models import Payment

app = Flask(__name__)
payment_obj = Payment()



@app.route("/payment")
def payment():
    data = payment_obj.all_payments()
    return jsonify(data)

@app.route("/create_payment", methods=["POST"])
def create_payment():
    payment_payload =  request.json
    payment_obj.set_payment(payment_payload= payment_payload)

    return jsonify({"payment_id":payment_payload["payment_id"],"stock_id":payment_payload["stock_id"],"count":payment_payload["count"],"price":payment_payload["price"]})


@app.route("/delete_payment", methods=["DELETE"])
def delete_payment():
    payment_payload =  request.json
    try:
        payment_obj.delete_payment(payment_id= payment_payload["payment_id"])
        return jsonify({'status':'OK'}), 200
    except:
        return jsonify({'status':'ERROR'}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5002)
