from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route("/payment/callback", methods=["POST"])
def mpesa_callback():
    data = request.get_json(silent=True)

    print("M-PESA CALLBACK RECEIVED:")
    print(data)

    return jsonify({
        "ResultCode": 0,
        "ResultDesc": "Accepted"
    }), 200


@app.route("/", methods=["GET"])
def health_check():
    return "Tutaide M-PESA callback server is running.", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)