from flask import Blueprint
from flask_simplelogin import login_required
from .views import (
    index, event_list, secret, only_admin, register, event_detail, checkout,
    user_list, approve_organizer, dashboard, event_form,
    event_delete, ticket_qr, ticket_list, ticket_cancel, revenue,
    scan_qr, checkin_process, api_check_ticket, admin_event_list, payment_result
)
from ticketselling.payment import bp as payment_bp


bp = Blueprint(
    "webui",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/webui/static"
)
admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

@admin_bp.before_request
@login_required(username="admin")
def before_request():
    pass

# --- URL RULES CHO WEBUI ---
bp.add_url_rule("/register", view_func=register, endpoint="register", methods=["GET", "POST"])
bp.add_url_rule("/", view_func=index)
bp.add_url_rule("/index", view_func=index)
bp.add_url_rule("/events/<int:event_id>", view_func=event_detail, endpoint="event_detail")
bp.add_url_rule("/events", view_func=event_list, endpoint="event_list")
bp.add_url_rule("/checkout", view_func=checkout, methods=["GET", "POST"])
bp.add_url_rule("/secret", view_func=secret, endpoint="secret")
bp.add_url_rule("/only_admin", view_func=only_admin, endpoint="onlyadmin")
bp.add_url_rule(
    "/payment/result",
    view_func=payment_result,
    endpoint="payment_result",
    methods=["GET"]
)

# --- URL RULES CHO ADMIN ---
admin_bp.add_url_rule("/", view_func=dashboard, endpoint="dashboard_main")
admin_bp.add_url_rule("/dashboard", view_func=dashboard, endpoint="dashboard")
admin_bp.add_url_rule("/users", view_func=user_list, endpoint="user_list")
admin_bp.add_url_rule("/users/<int:user_id>/approve", view_func=approve_organizer, endpoint="approve_organizer", methods=["POST"])
admin_bp.add_url_rule("/events", view_func=admin_event_list, endpoint="event_list")
admin_bp.add_url_rule("/events/<int:event_id>/delete", view_func=event_delete, endpoint="event_delete", methods=["POST"])
admin_bp.add_url_rule("/events/new", view_func=event_form, endpoint="event_form_new", methods=["POST", "GET"])
admin_bp.add_url_rule("/events/<int:event_id>/edit", view_func=event_form, endpoint="event_form_edit", methods=["POST", "GET"])
admin_bp.add_url_rule("/tickets", view_func=ticket_list, endpoint="ticket_list")
admin_bp.add_url_rule("/tickets/<int:ticket_id>/qr", view_func=ticket_qr, endpoint="ticket_qr")
admin_bp.add_url_rule("/tickets/<int:ticket_id>/cancel", view_func=ticket_cancel, endpoint="ticket_cancel", methods=["POST"])
admin_bp.add_url_rule("/revenue", view_func=revenue, endpoint="revenue")
admin_bp.add_url_rule("/checkin/scan", view_func=scan_qr, endpoint="scan_qr", methods=["GET"])
admin_bp.add_url_rule("/api/check-ticket", view_func=api_check_ticket, endpoint="api_check_ticket", methods=["POST"])

def init_app(app):
    app.register_blueprint(bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(payment_bp)
