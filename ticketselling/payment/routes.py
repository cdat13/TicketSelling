from flask import redirect

from . import bp

from .vnpay import create_payment


@bp.route("/create", methods=["POST"])
def payment_create():
    return create_payment()

@bp.route("/return")
def payment_return():

    return "Payment Return"