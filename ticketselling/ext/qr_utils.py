import base64
from io import BytesIO

import qrcode
from itsdangerous import URLSafeSerializer, BadSignature
from flask import current_app

QR_SALT = "ticket-qr-v1"


def _serializer():
    return URLSafeSerializer(current_app.config["SECRET_KEY"], salt=QR_SALT)


def sign_ticket_code(ticket_code: str) -> str:
    return _serializer().dumps({"code": ticket_code})


def verify_qr_token(token: str):
    try:
        data = _serializer().loads(token)
        return data.get("code")
    except (BadSignature, Exception):
        return None


def generate_qr_base64_png(payload: str) -> str:
    img = qrcode.make(payload)
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode("ascii")