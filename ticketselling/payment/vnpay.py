import hashlib
import hmac
import urllib.parse

from datetime import datetime
from flask import redirect, request, url_for


VNPAY_URL = "https://sandbox.vnpayment.vn/paymentv2/vpcpay.html"


def create_payment():
    amount = 10000

    tmn_code = "LHD1JD82"
    hash_secret = "TEVZXVUASYYJQMWBDZRKVKASTELDKIAN"

    if not tmn_code:
        return "Chưa cấu hình VNPAY_TMN_CODE.", 500

    if not hash_secret:
        return "Chưa cấu hình VNPAY_HASH_SECRET.", 500

    tmn_code = tmn_code.strip()
    hash_secret = hash_secret.strip()

    # Thời gian Việt Nam
    from zoneinfo import ZoneInfo
    now = datetime.now(ZoneInfo("Asia/Ho_Chi_Minh"))

    txn_ref = "TEST" + now.strftime("%Y%m%d%H%M%S")

    # Lấy IP client
    client_ip = request.headers.get("X-Forwarded-For")

    if client_ip:
        client_ip = client_ip.split(",")[0].strip()
    else:
        client_ip = request.remote_addr or "127.0.0.1"

    params = {
        "vnp_Version": "2.1.0",
        "vnp_Command": "pay",
        "vnp_TmnCode": tmn_code,
        "vnp_Amount": str(int(amount * 100)),
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

    # Sort theo tên parameter
    params = dict(sorted(params.items()))

    # =========================
    # TẠO CHUỖI HASH
    # =========================

    hash_data = "&".join(
        f"{key}={value}"
        for key, value in params.items()
        if value is not None and value != ""
    )

    # HMAC SHA512
    secure_hash = hmac.new(
        hash_secret.encode("utf-8"),
        hash_data.encode("utf-8"),
        hashlib.sha512
    ).hexdigest()

    # =========================
    # TẠO QUERY STRING
    # =========================

    query_string = urllib.parse.urlencode(
        params,
        quote_via=urllib.parse.quote
    )

    payment_url = (
        VNPAY_URL
        + "?"
        + query_string
        + "&vnp_SecureHash="
        + secure_hash
    )

    # DEBUG
    print("========== VNPAY DEBUG ==========")
    print("TMN CODE:", tmn_code)
    print("TXN REF:", txn_ref)
    print("IP:", client_ip)
    print("RETURN URL:", params["vnp_ReturnUrl"])
    print("HASH DATA:", hash_data)
    print("SECURE HASH:", secure_hash)
    print("PAYMENT URL:", payment_url)
    print("=================================")

    return redirect(payment_url)