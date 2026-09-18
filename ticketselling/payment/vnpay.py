import os
import hashlib
import hmac
import urllib.parse

from datetime import datetime
from flask import redirect, request, url_for


VNPAY_URL = "https://sandbox.vnpayment.vn/paymentv2/vpcpay.html"


def create_payment():

    amount = 10000

    tmn_code = C267DLWSs
    hash_secret = RCZB1B6FHJZAWP83LT84G4W81NPOAT3I

    vnpay_url = os.getenv(
        "VNPAY_URL",
        VNPAY_URL
    )

    if not tmn_code:
        return "Chưa cấu hình VNPAY_TMN_CODE.", 500

    if not hash_secret:
        return "Chưa cấu hình VNPAY_HASH_SECRET.", 500

    now = datetime.now()

    txn_ref = "TEST" + now.strftime("%Y%m%d%H%M%S")

    params = {
        "vnp_Version": "2.1.0",
        "vnp_Command": "pay",
        "vnp_TmnCode": tmn_code,
        "vnp_Amount": int(amount * 100),
        "vnp_CurrCode": "VND",
        "vnp_TxnRef": txn_ref,
        "vnp_OrderInfo": "Thanh_toan_demo_VNPAY",
        "vnp_OrderType": "other",
        "vnp_Locale": "vn",
        "vnp_ReturnUrl": url_for(
            "webui.payment_result",
            _external=True
        ),
        "vnp_IpAddr": request.remote_addr or "127.0.0.1",
        "vnp_CreateDate": now.strftime("%Y%m%d%H%M%S"),
    }

    params = dict(sorted(params.items()))

    hash_data = urllib.parse.urlencode(
        params,
        quote_via=urllib.parse.quote
    )

    secure_hash = hmac.new(
        hash_secret.encode("utf-8"),
        hash_data.encode("utf-8"),
        hashlib.sha512
    ).hexdigest()

    query_string = urllib.parse.urlencode(
        params,
        quote_via=urllib.parse.quote
    )

    payment_url = (
        vnpay_url
        + "?"
        + query_string
        + "&vnp_SecureHash="
        + secure_hash
    )

    return redirect(payment_url)