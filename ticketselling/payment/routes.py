from flask import redirect

from . import bp


@bp.route("/create")
def create_payment():

    return "Create Payment"


@bp.route("/return")
def payment_return():

    return "Payment Return"