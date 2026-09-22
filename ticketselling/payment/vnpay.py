import os
import hashlib
import hmac
import urllib.parse

from datetime import datetime
from zoneinfo import ZoneInfo

from flask import redirect, request, url_for


VNPAY_URL = "https://sandbox.vnpayment.vn/paymentv2/vpcpay.html"


def create_payment():

    # Số tiền demo: 10.000 VND
    amount = 10000

    # Lấy từ Environment Variables trên Render
    tmn_code = os.getenv("VNPAY_TMN_CODE")
    hash_secret = os.getenv("VNPAY_HASH_SECRET")
    vnpay_url = os.getenv("VNPAY_URL", VNPAY_URL)

    if not tmn_code:
        return "Chưa cấu hình VNPAY_TMN_CODE.", 500

    if not hash_secret:
        return "Chưa cấu hình VNPAY_HASH_SECRET.", 500

    tmn_code = tmn_code.strip()
    hash_secret = hash_secret.strip()

    # Thời gian Việt Nam GMT+7
    now = datetime.now(ZoneInfo("Asia/Ho_Chi_Minh"))

    # Mã giao dịch duy nhất
    txn_ref = "TEST" + now.strftime("%Y%m%d%H%M%S")

    # Lấy IP client
    client_ip = request.headers.get(
        "X-Forwarded-For",
        request.remote_addr
    )

    if client_ip:
        client_ip = client_ip.split(",")[0].strip()

    client_ip = client_ip or "127.0.0.1"

    params = {
        "vnp_Version": "2.1.0",
        "vnp_Command": "pay",
        "vnp_TmnCode": tmn_code,
        "vnp_Amount": str(amount * 100),
        "vnp_CurrCode": "VND",
        "vnp_TxnRef": txn_ref,
        "vnp_OrderInfo": "Thanh_toan_demo_VNPAY",
        "vnp_OrderType": "other",
        "vnp_Locale": "vn",
        "vnp_ReturnUrl": url_for(
            "webui.payment_result",
            _external=True
        ),
        "vnp_IpAddr": client_ip,
        "vnp_CreateDate": now.strftime("%Y%m%d%H%M%S"),
    }

    # ==========================================
    # 1. SORT PARAMS THEO ALPHABET
    # ==========================================
    params = dict(sorted(params.items()))

    # ==========================================
    # 2. TẠO HASH DATA
    # KHÔNG URL-ENCODE
    # ==========================================
    hash_data = "&".join(
        f"{key}={value}"
        for key, value in params.items()
        if value is not None and value != ""
    )

    # ==========================================
    # 3. HMAC SHA512
    # ==========================================
    secure_hash = hmac.new(
        hash_secret.encode("utf-8"),
        hash_data.encode("utf-8"),
        hashlib.sha512
    ).hexdigest()

    # ==========================================
    # 4. TẠO QUERY STRING
    # URL-ENCODE Ở BƯỚC NÀY
    # ==========================================
    query_string = urllib.parse.urlencode(params)

    payment_url = (
        f"{vnpay_url}"
        f"?{query_string}"
        f"&vnp_SecureHash={secure_hash}"
    )

    # DEBUG - không in hash_secret
    print("========== VNPAY DEBUG ==========")
    print("TMN CODE:", tmn_code)
    print("TXN REF:", txn_ref)
    print("RETURN URL:", params["vnp_ReturnUrl"])
    print("HASH DATA:", hash_data)
    print("SECURE HASH:", secure_hash)
    print("=================================")

    return redirect(payment_url)