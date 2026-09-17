import base64

import pytest
from flask import Flask

from ticketselling.ext.qr_utils import (
    generate_qr_base64_png,
    sign_ticket_code,
    verify_qr_token,
)


@pytest.fixture
def qr_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "unit-test-secret-key"
    return app


def test_sign_and_verify_ticket_code(qr_app):
    with qr_app.app_context():
        token = sign_ticket_code("TICKET-001")

        assert verify_qr_token(token) == "TICKET-001"


def test_verify_tampered_token_returns_none(qr_app):
    with qr_app.app_context():
        token = sign_ticket_code("TICKET-001")

        assert verify_qr_token(f"{token}tampered") is None


@pytest.mark.parametrize("invalid_token", ["", "not-a-valid-token", "abc.def"])
def test_verify_invalid_token_returns_none(qr_app, invalid_token):
    with qr_app.app_context():
        assert verify_qr_token(invalid_token) is None


def test_token_signed_with_different_secret_is_rejected():
    signing_app = Flask("signing-app")
    signing_app.config["SECRET_KEY"] = "signing-secret"
    with signing_app.app_context():
        token = sign_ticket_code("TICKET-001")

    verifying_app = Flask("verifying-app")
    verifying_app.config["SECRET_KEY"] = "different-secret"
    with verifying_app.app_context():
        assert verify_qr_token(token) is None


def test_generate_qr_base64_png_returns_valid_png():
    encoded_image = generate_qr_base64_png("TICKET-001")

    image_bytes = base64.b64decode(encoded_image, validate=True)

    assert image_bytes.startswith(b"\x89PNG\r\n\x1a\n")
    assert len(image_bytes) > 8
