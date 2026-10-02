import os
import requests
import base64
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# ==================================================
# CONFIGURATION - loaded from .env
# MPESA_ENV controls sandbox vs production
# ==================================================

CONSUMER_KEY = os.getenv("MPESA_CONSUMER_KEY")
CONSUMER_SECRET = os.getenv("MPESA_CONSUMER_SECRET")
SHORTCODE = os.getenv("MPESA_SHORTCODE")
PASSKEY = os.getenv("MPESA_PASSKEY")

MPESA_ENV = os.getenv("MPESA_ENV", "sandbox")

if MPESA_ENV == "production":
    BASE_URL = "https://api.safaricom.co.ke"
else:
    BASE_URL = "https://sandbox.safaricom.co.ke"

# This MUST be a publicly reachable URL once deployed
# (not localhost) - Safaricom sends payment confirmations here
CALLBACK_URL = "https://tutaide.co/mpesa/callback"


def get_access_token():

    url = f"{BASE_URL}/oauth/v1/generate?grant_type=client_credentials"

    response = requests.get(
        url,
        auth=(CONSUMER_KEY, CONSUMER_SECRET)
    )

    response.raise_for_status()

    return response.json()["access_token"]


def initiate_stk_push(phone_number, amount, account_reference, transaction_desc):

    access_token = get_access_token()

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    password = base64.b64encode(
        f"{SHORTCODE}{PASSKEY}{timestamp}".encode("utf-8")
    ).decode("utf-8")

    url = f"{BASE_URL}/mpesa/stkpush/v1/processrequest"

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    payload = {
        "BusinessShortCode": SHORTCODE,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": int(amount),
        "PartyA": phone_number,
        "PartyB": SHORTCODE,
        "PhoneNumber": phone_number,
        "CallBackURL": CALLBACK_URL,
        "AccountReference": account_reference,
        "TransactionDesc": transaction_desc
    }

    response = requests.post(
        url,
        json=payload,
        headers=headers
    )

    response.raise_for_status()

    return response.json()


def query_stk_push_status(checkout_request_id):

    access_token = get_access_token()

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    password = base64.b64encode(
        f"{SHORTCODE}{PASSKEY}{timestamp}".encode("utf-8")
    ).decode("utf-8")

    url = f"{BASE_URL}/mpesa/stkpushquery/v1/query"

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    payload = {
        "BusinessShortCode": SHORTCODE,
        "Password": password,
        "Timestamp": timestamp,
        "CheckoutRequestID": checkout_request_id
    }

    response = requests.post(
        url,
        json=payload,
        headers=headers
    )

    if response.status_code != 200:

        # Common sandbox behaviour: querying too soon after
        # initiating returns a 500 meaning "still processing"
        # rather than a real failure.
        return "pending"

    result = response.json()

    result_code = result.get("ResultCode")

    if result_code in (0, "0"):
        return "success"

    elif result_code in (None, 1032, "1032"):
        return "pending"

    else:
        return "failed"