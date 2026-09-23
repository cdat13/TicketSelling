import os
import hashlib
import hmac
import urllib.parse
import json
from datetime import datetime
from datetime import datetime, timedelta
from flask import redirect, request, url_for, session, flash
from ticketselling.ext.database import db
from ticketselling.models import Order

VNPAY_URL = "https://sandbox.vnpayment.vn/paymentv2/vpcpay.html"


def create_payment():

    checkout_data = session.get("checkout_data")
    if not checkout_data:
        flash("Không có thông tin đơn hàng, vui lòng chọn vé lại.", "warning")
        return redirect(url_for("webui.index"))

    amount = int(round(float(checkout_data["total_amount"])))
    if amount <= 0:
        flash("Số tiền thanh toán không hợp lệ.", "danger")
        return redirect(url_for("webui.index"))

    tmn_code = os.getenv("VNPAY_TMN_CODE")
    hash_secret = os.getenv("VNPAY_HASH_SECRET")

    if not tmn_code:
        return "Chưa cấu hình VNPAY_TMN_CODE.", 500

    if not hash_secret:
        return "Chưa cấu hình VNPAY_HASH_SECRET.", 500

    tmn_code = tmn_code.strip()
    hash_secret = hash_secret.strip()

    now = datetime.utcnow() + timedelta(hours=7)
    txn_ref = "TEST" + now.strftime("%Y%m%d%H%M%S")

    order = Order(
        order_code=txn_ref,
        customer_name=request.form.get("customer_name", "").strip(),
        email=request.form.get("email", "").strip(),
        phone=request.form.get("phone", "").strip(),
        total_amount=amount,
        ticket_quantity=sum(i["quantity"] for i in checkout_data["items"]),
        note=json.dumps({
            "event_id": checkout_data["event_id"],
            "items": checkout_data["items"],
        }),
        payment_method="VNPAY",
        payment_status="Pending",
        vnp_txn_ref=txn_ref,
    )
    db.session.add(order)
    db.session.commit()

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
        "vnp_IpAddr": request.remote_addr or "127.0.0.1",
        "vnp_CreateDate": now.strftime("%Y%m%d%H%M%S"),
    }

    sorted_params = sorted(params.items())

    hash_data = "&".join(
        urllib.parse.quote_plus(str(key))
        + "="
        + urllib.parse.quote_plus(str(value))
        for key, value in sorted_params
        if value is not None and value != ""
    )

    secure_hash = hmac.new(
        hash_secret.encode("utf-8"),
        hash_data.encode("utf-8"),
        hashlib.sha512
    ).hexdigest()

    query_string = urllib.parse.urlencode(
        dict(sorted_params)
    )

    payment_url = (
        VNPAY_URL
        + "?"
        + query_string
        + "&vnp_SecureHash="
        + secure_hash
    )

    print("VNPAY CREATE PAYMENT", flush=True)
    print("TMN:", tmn_code, flush=True)
    print("HASH:", secure_hash, flush=True)

    return redirect(payment_url)