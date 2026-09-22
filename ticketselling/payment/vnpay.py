import os
import hashlib
import hmac
import urllib.parse

from datetime import datetime
from zoneinfo import ZoneInfo

from flask import redirect, request, url_for


VNPAY_URL = "https://sandbox.vnpayment.vn/paymentv2/vpcpay.html"


def create_payment():
    amount = 10000

    tmn_code = "C267DLWS"
    hash_secret = "RCZB1B6FHJZAWP83LT84G4W81NPOAT3I"

    if not tmn_code:
        return "Chưa cấu hình VNPAY_TMN_CODE.", 500

    if not hash_secret:
        return "Chưa cấu hình VNPAY_HASH_SECRET.", 500

    tmn_code = tmn_code.strip()
    hash_secret = hash_secret.strip()

    now = datetime.now()

    txn_ref = "TEST" + now.strftime("%Y%m%d%H%M%S")

    # Lấy IP thật phía client nếu Render đang reverse proxy
    client_ip = request.headers.get("X-Forwarded-For")

    if client_ip:
        client_ip = client_ip.split(",")[0].strip()
    else:
        client_ip = request.remote_addr or "127.0.0.1"

    params = {
        "vnp_Version": "2.1.0",
        "vnp_Command": "pay",
        "vnp_TmnCode": tmn_code,
        "vnp_Amount": str(amount * 100),
        "vnp_CurrCode": "VND",
        "vnp_TxnRef": txn_ref,
        "vnp_OrderInfo": "Thanh toan demo VNPAY",
        "vnp_OrderType": "other",
        "vnp_Locale": "vn",
        "vnp_ReturnUrl": url_for(
            "webui.payment_result",
            _external=True
        ),
        "vnp_IpAddr": client_ip,
        "vnp_CreateDate": now.strftime("%Y%m%d%H%M%S"),
    }

    # Sort alphabet
    params = dict(sorted(params.items()))

    # =====================================
    # HASH DATA - KHÔNG URL ENCODE
    # =====================================
    hash_data = "&".join(
        f"{key}={value}"
        for key, value in params.items()
        if value is not None and value != ""
    )

    secure_hash = hmac.new(
        hash_secret.encode("utf-8"),
        hash_data.encode("utf-8"),
        hashlib.sha512
    ).hexdigest()

    # =====================================
    # QUERY STRING - URL ENCODE
    # =====================================
    query_string = urllib.parse.urlencode(params)

    payment_url = (
        "https://sandbox.vnpayment.vn/paymentv2/vpcpay.html?"
        + query_string
        + "&vnp_SecureHash="
        + secure_hash
    )

    print("========== VNPAY DEBUG ==========", flush=True)
    print("TMN CODE:", tmn_code, flush=True)
    print("TXN REF:", txn_ref, flush=True)
    print("IP:", client_ip, flush=True)
    print("RETURN URL:", params["vnp_ReturnUrl"], flush=True)
    print("HASH DATA:", hash_data, flush=True)
    print("SECURE HASH:", secure_hash, flush=True)
    print("=================================", flush=True)

    return redirect(payment_url)