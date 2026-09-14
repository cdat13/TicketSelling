from flask import Blueprint
from .views import index, only_admin, secret, register, checkout,create_payment, payment_result
from ticketselling.payment import bp as payment_bp
from .views import event_detail, event_list

bp = Blueprint(
    "webui",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/webui/static"
)

bp.add_url_rule("/register", view_func=register, endpoint="register", methods= ["GET", "POST"])

bp.add_url_rule("/", view_func=index)
bp.add_url_rule("/index", view_func=index)
bp.add_url_rule("/events/<int:event_id>", view_func= event_detail, endpoint="event_detail")
bp.add_url_rule( "/events",view_func=event_list,endpoint="event_list")

bp.add_url_rule(
    "/checkout",
    view_func=checkout,
    methods=["GET", "POST"]
)

bp.add_url_rule("/secret", view_func=secret, endpoint="secret")
bp.add_url_rule("/only_admin", view_func=only_admin, endpoint="onlyadmin")

bp.add_url_rule(
    "/payment/create",
    view_func=create_payment,
    methods=["POST"]
)

bp.add_url_rule(
    "/payment/result",
    view_func=payment_result
)

def init_app(app):
    app.register_blueprint(bp)
    app.register_blueprint(payment_bp)