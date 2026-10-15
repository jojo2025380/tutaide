import logging
from flask import Flask, request, jsonify
from database import record_mpesa_callback

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.route("/payment/callback", methods=["POST"])

def mpesa_callback():
    
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "ResultCode": 1,
            "ResultDesc": "Invalid callback payload"
        }), 400

    body = data.get("Body")
    if not isinstance(body, dict):
        return jsonify({
            "ResultCode": 1,
            "ResultDesc": "Missing callback body"
        }), 400

    stk_callback = body.get("stkCallback")
    if not isinstance(stk_callback, dict):
        return jsonify({
            "ResultCode": 1,
            "ResultDesc": "Missing STK callback data"
        }), 400

    checkout_id = stk_callback.get("CheckoutRequestID")
    result_code = stk_callback.get("ResultCode")

    if not checkout_id or result_code is None:
        return jsonify({
            "ResultCode": 1,
            "ResultDesc": "Missing required callback fields"
        }), 400

    # Failed or cancelled payments must not be recorded as successful.
    if str(result_code) != "0":
        logger.info("M-PESA reported a non-success result.")
        return jsonify({
            "ResultCode": 0,
            "ResultDesc": "Callback received"
        }), 200

    metadata = stk_callback.get("CallbackMetadata")
    items = metadata.get("Item") if isinstance(metadata, dict) else None

    if not isinstance(items, list):
        logger.warning("Successful callback missing transaction metadata.")
        return jsonify({
            "ResultCode": 1,
            "ResultDesc": "Missing transaction metadata"
        }), 400

    details = {
        item.get("Name"): item.get("Value")
        for item in items
        if isinstance(item, dict) and item.get("Name")
    }

    amount = details.get("Amount")
    receipt = details.get("MpesaReceiptNumber")

    if amount is None or not receipt:
        logger.warning("Successful callback missing amount or receipt.")
        return jsonify({
            "ResultCode": 1,
            "ResultDesc": "Missing amount or receipt"
        }), 400

    try:
        recorded = record_mpesa_callback(
            checkout_id,
            amount,
            receipt
        )
    except Exception:
        logger.exception("Could not record M-PESA callback.")
        return jsonify({
            "ResultCode": 1,
            "ResultDesc": "Could not record callback"
        }), 500

    if not recorded:
        logger.warning(
            "Callback did not match a pending payment or expected amount."
        )
        return jsonify({
            "ResultCode": 1,
            "ResultDesc": "Payment did not match a pending record"
        }), 400

    logger.info("M-PESA callback details recorded.")
    return jsonify({
        "ResultCode": 0,
        "ResultDesc": "Accepted"
    }), 200


@app.route("/", methods=["GET"])
def health_check():
    return "TutAide M-PESA callback server is running.", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
