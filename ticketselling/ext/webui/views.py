from collections import defaultdict

from flask_simplelogin import login_required
from ticketselling.models import EventCategory
from ticketselling.ext.auth import create_user

from datetime import datetime, timedelta
from flask import render_template, request, redirect, url_for, flash, session
from ticketselling.ext.database import db
from ticketselling.models import Event, Ticket, User
from ticketselling.ext.qr_utils import generate_qr_base64_png
from flask import jsonify
import os
import urllib.parse
import hmac
import hashlib
from datetime import datetime


from dotenv import load_dotenv

load_dotenv()



def index():
    keyword = request.args.get("keyword", "").strip()
    location = request.args.get("location", "").strip()
    category = request.args.get("category", "").strip()

    query = Event.query.filter(
        Event.status == "ACTIVE"
    )

    if keyword:
        query = query.filter(
            Event.name.ilike(f"%{keyword}%")
        )

    if location:
        query = query.filter(
            Event.location.ilike(f"%{location}%")
        )

    if category:
        query = query.filter(
            Event.category_id == int(category)
        )

    events = query.order_by(
        Event.start_time
    ).all()

    featured_events = (
        Event.query
        .filter(Event.status == "ACTIVE")
        .order_by(Event.id.asc())
        .limit(4)
        .all()
    )

    raw_locations = (
        Event.query
        .with_entities(Event.location)
        .filter(Event.location.isnot(None))
        .distinct()
        .all()
    )

    locations = sorted({
        item[0].split(",")[-1].strip()
        for item in raw_locations
        if item[0]
    })

    categories = (
        EventCategory.query
        .order_by(EventCategory.name)
        .all()
    )

    return render_template(
        "index.html",
        events=events,
        featured_events=featured_events,
        categories=categories,
        locations=locations,
        keyword=keyword,
        selected_location=location,
        selected_category=int(category)
        if category else None
    )


def event_list():

    keyword = request.args.get(
        "keyword", ""
    ).strip()

    location = request.args.get(
        "location", ""
    )

    category = request.args.get(
        "category", ""
    )

    query = Event.query.filter(
        Event.status == "ACTIVE"
    )

    if keyword:
        query = query.filter(
            Event.name.ilike(
                f"%{keyword}%"
            )
        )

    if location:
        query = query.filter(
            Event.location.ilike(
                f"%{location}%"
            )
        )

    if category:
        query = query.filter(
            Event.category_id == int(category)
        )

    events = (
        query
        .order_by(Event.start_time)
        .all()
    )

    locations = (
        Event.query
        .with_entities(Event.location)
        .filter(Event.location.isnot(None))
        .distinct()
        .all()
    )

    locations = sorted(
        [
            x[0].strip()
            for x in locations
            if x[0]
        ]
    )

    categories = EventCategory.query.all()

    return render_template(
        "event/list.html",
        events=events,
        keyword=keyword,
        categories=categories,
        locations=locations,
        selected_location=location,
        selected_category=int(category)
        if category else None
    )

@login_required
def secret():
    return "This can be seen only if user is logged in"


@login_required(username="admin")
def only_admin():
    return "only admin user can see this text"

def register():

    err_msg = None

    if request.method == "POST":

        full_name = request.form.get(
            "full_name", ""
        ).strip()

        email = request.form.get(
            "email", ""
        ).strip().lower()

        username = request.form.get(
            "username", ""
        ).strip()

        password = request.form.get(
            "password", ""
        )

        confirm = request.form.get(
            "confirm", ""
        )

        if not all([
            full_name,
            email,
            username,
            password,
            confirm
        ]):
            err_msg = (
                "Vui lòng nhập đầy đủ thông tin."
            )

        elif "@" not in email:
            err_msg = (
                "Địa chỉ email không hợp lệ."
            )

        elif len(username) < 3:
            err_msg = (
                "Tên đăng nhập phải có ít nhất 3 ký tự."
            )

        elif len(password) < 6:
            err_msg = (
                "Mật khẩu phải có ít nhất 6 ký tự."
            )

        elif password != confirm:
            err_msg = (
                "Mật khẩu xác nhận không khớp."
            )

        else:

            try:

                create_user(
                    full_name=full_name,
                    email=email,
                    username=username,
                    password=password,
                )

                return redirect(
                    url_for(
                        "simplelogin.login"
                    )
                )

            except RuntimeError as ex:

                err_msg = str(ex)

            except Exception:

                err_msg = (
                    "Không thể tạo tài khoản. "
                    "Vui lòng thử lại."
                )

    return render_template(
        "auth/register.html",
        err_msg=err_msg,
    )


def event_detail(event_id):

    event = (
        Event.query
        .filter_by(
            id=event_id,
            status="ACTIVE"
        )
        .first()
    )

    if event is None:

        flash(
            "Sự kiện không tồn tại "
            "hoặc hiện không khả dụng.",
            "warning"
        )

        return redirect(
            url_for("webui.index")
        )

    return render_template(
        "event/detail.html",
        event=event
    )



@login_required
@login_required
def checkout():

    if request.method == "POST":

        event_id = request.form.get("event_id", type=int)

        if not event_id:
            flash("Không xác định được sự kiện.", "danger")
            return redirect(url_for("webui.index"))

        event = Event.query.get_or_404(event_id)

        selected_items = []
        total_amount = 0

        # Lấy số lượng vé từ form
        for ticket_type in event.ticket_types:

            field_name = f"ticket_{ticket_type.id}"
            quantity = request.form.get(field_name, 0, type=int)

            if quantity < 0:
                quantity = 0

            if quantity == 0:
                continue

            # Kiểm tra tồn kho
            if quantity > ticket_type.current_stock:
                flash(
                    f"Loại vé '{ticket_type.name}' chỉ còn "
                    f"{ticket_type.current_stock} vé.",
                    "danger"
                )
                return redirect(
                    url_for(
                        "webui.event_detail",
                        event_id=event.id
                    )
                )

            item_total = quantity * ticket_type.price
            total_amount += item_total

            selected_items.append({
                "ticket_type_id": ticket_type.id,
                "name": ticket_type.name,
                "price": ticket_type.price,
                "quantity": quantity,
                "subtotal": item_total
            })

        # Không chọn vé nào
        if not selected_items:
            flash("Vui lòng chọn ít nhất một vé.", "warning")
            return redirect(
                url_for(
                    "webui.event_detail",
                    event_id=event.id
                )
            )

        # Lưu thông tin checkout vào session
        session["checkout_data"] = {
            "event_id": event.id,
            "items": [
                {
                    "ticket_type_id": item["ticket_type_id"],
                    "quantity": item["quantity"]
                }
                for item in selected_items
            ],
            "total_amount": total_amount
        }

        return render_template(
            "checkout/checkout.html",
            event=event,
            selected_items=selected_items,
            total_amount=total_amount
        )

    # GET /checkout
    checkout_data = session.get("checkout_data")

    if not checkout_data:
        flash("Chưa có thông tin vé.", "warning")
        return redirect(url_for("webui.index"))

    event = Event.query.get_or_404(
        checkout_data["event_id"]
    )

    selected_items = []

    for item in checkout_data["items"]:

        ticket_type = next(
            (
                ticket
                for ticket in event.ticket_types
                if ticket.id == item["ticket_type_id"]
            ),
            None
        )

        if not ticket_type:
            continue

        quantity = item["quantity"]

        selected_items.append({
            "ticket_type_id": ticket_type.id,
            "name": ticket_type.name,
            "price": ticket_type.price,
            "quantity": quantity,
            "subtotal": quantity * ticket_type.price
        })

    total_amount = sum(
        item["subtotal"]
        for item in selected_items
    )

    return render_template(
        "checkout/checkout.html",
        event=event,
        selected_items=selected_items,
        total_amount=total_amount
    )

def approve_organizer(user_id):
    user = User.query.get_or_404(user_id)
    if user.role == "pending_organizer":
        user.role = "organizer"
        db.session.commit()
        flash(f"Đã duyệt cấp quyền Nhà tổ chức cho: {user.username}!", "success")
    else:
        flash("Tài khoản này không nằm trong danh sách chờ duyệt.", "warning")

    return redirect(url_for("admin.user_list"))

def dashboard():
    total_events = Event.query.filter_by(status="ACTIVE").count()
    active_tickets = Ticket.query.filter(Ticket.status != "cancelled").all()
    return render_template(
        "admin/dashboard.html",
        total_events=total_events,
        tickets_sold=len(active_tickets),
        revenue=sum(t.event.ticket_price for t in active_tickets),
    )

def admin_event_list():
    events = Event.query.order_by(Event.id.desc()).all()
    return render_template("admin/event_list.html", events=events)

def user_list():
    return render_template("admin/user_list.html", users=User.query.order_by(User.id.desc()).all())

def event_form(event_id=None):
    event = Event.query.get_or_404(event_id) if event_id else None
    organizers = User.query.filter_by(role="organizer").all()

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        date_str = request.form.get("date")

        if not name or not date_str:
            flash("Vui lòng nhập đầy đủ tên sự kiện và ngày giờ tổ chức.", "danger")
            return render_template("admin/event_form.html", event=event, organizers=organizers)

        try:
            start_dt = datetime.strptime(date_str, "%Y-%m-%dT%H:%M")
        except ValueError:
            flash("Định dạng ngày giờ không hợp lệ.", "danger")
            return render_template("admin/event_form.html", event=event, organizers=organizers)

        if event is None:
            event = Event()
            db.session.add(event)

        event.name = request.form.get("name").strip()
        event.description = request.form.get("description", "").strip()
        event.location = request.form.get("location", "").strip()
        event.start_time = start_dt
        event.ticket_capacity = int(request.form.get("ticket_capacity") or 0)
        event.ticket_price = int(request.form.get("ticket_price") or 0)
        event.status = request.form.get("status","DRAFT")
        event.organizer_id = int(request.form.get("organizer_id")) if request.form.get("organizer_id") else None

        db.session.commit()
        flash(f"Đã lưu sự kiện '{event.name}'.", "success")
        return redirect(url_for("admin.event_list"))

    return render_template("admin/event_form.html", event=event, organizers=organizers)

def event_delete(event_id):
    event = Event.query.get_or_404(event_id)
    db.session.delete(event)
    db.session.commit()
    flash("Đã xoá sự kiện.", "info")
    return redirect(url_for("admin.event_list"))

def ticket_qr(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    qr_base64 = generate_qr_base64_png(ticket.ticket_code)
    return render_template("admin/ticket_qr.html", ticket=ticket, qr_base64=qr_base64)

def ticket_list():
    status_filter = request.args.get("status", "")
    event_filter = request.args.get("event_id", "")

    query = Ticket.query
    if status_filter:
        query = query.filter_by(status=status_filter)
    if event_filter:
        query = query.filter_by(event_id=event_filter)

    tickets = query.order_by(Ticket.created_at.desc()).all()
    events = Event.query.order_by(Event.name.asc()).all()
    return render_template(
        "admin/ticket_list.html",
        tickets=tickets,
        events=events,
        status_filter=status_filter,
        event_filter=event_filter,
    )

def ticket_cancel(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)

    if ticket.status == "used":
        flash("Vé đã sử dụng, không thể hủy.", "danger")
        return redirect(url_for("webui.ticket_list"))

    time_since_bought = datetime.now() - ticket.created_at
    if time_since_bought > timedelta(hours=24):
        flash("Đã quá 24h, bạn không thể hủy vé này nữa.", "warning")
        return redirect(url_for("webui.ticket_list"))

    ticket.status = "cancelled"
    db.session.commit()
    flash("Hủy vé thành công.", "success")
    return redirect(url_for("webui.ticket_list"))

def revenue():
    active_tickets = Ticket.query.filter(Ticket.status != "cancelled").all()
    organizer_stats = defaultdict(int)
    grand_total = 0
    organizer_stats = {}

    for ticket in active_tickets:
        evt = ticket.event
        grand_total += evt.ticket_price
        org_name = evt.organizer.username if evt.organizer else "Admin (Nội bộ)"

        if org_name not in organizer_stats:
            organizer_stats[org_name] = {
                "sold": 0,
                "revenue": 0,
                "events_list": set()
            }

        organizer_stats[org_name]["sold"] += 1
        organizer_stats[org_name]["revenue"] += evt.ticket_price
        organizer_stats[org_name]["events_list"].add(evt.name)

    return render_template("admin/revenue.html",
                           organizer_stats=organizer_stats,
                           grand_total=grand_total)

def scan_qr():
    return render_template("checkin/scan_qr.html")

def checkin_process():
    ticket_code = request.form.get("ticket_code", "").strip()
    if not ticket_code:
        flash("Không đọc được mã vé, vui lòng thử lại.", "warning")
        return redirect(url_for("webui.scan_qr"))

    ticket = Ticket.query.filter_by(ticket_code=ticket_code).first()

    if not ticket:
        flash("Mã vé không tồn tại trong hệ thống!", "danger")
    elif ticket.status == "cancelled":
        flash("Cảnh báo: Vé này đã bị huỷ!", "danger")
    elif ticket.status == "used":
        check_time = ticket.checked_in_at.strftime("%H:%M %d/%m/%Y") if ticket.checked_in_at else "trước đó"
        flash(f"Cảnh báo: Vé đã bị sử dụng vào lúc {check_time}!", "warning")
    else:
        ticket.status = "used"
        ticket.checked_in_at = datetime.now()
        db.session.commit()
        flash(f"Soát vé thành công! Khách: {ticket.holder_name} - Sự kiện: {ticket.event.name}", "success")

    return redirect(url_for("webui.scan_qr"))

def api_check_ticket():
    data = request.get_json() or {}
    ticket_code = data.get("ticket_code", "").strip()

    if not ticket_code:
        return jsonify({"valid": False, "message": "Không nhận được mã vé!"}), 400

    ticket = Ticket.query.filter_by(ticket_code=ticket_code).first()

    if not ticket:
        return jsonify({"valid": False, "message": "Mã vé không tồn tại!"})

    if ticket.status == "cancelled":
        return jsonify({
            "valid": False,
            "message": "Vé này đã bị hủy!",
            "customer_name": ticket.holder_name
        })

    if ticket.status == "used":
        check_time = ticket.checked_in_at.strftime("%H:%M %d/%m/%Y") if ticket.checked_in_at else "trước đó"
        return jsonify({
            "valid": False,
            "message": f"Vé đã được sử dụng lúc {check_time}!",
            "customer_name": ticket.holder_name
        })

    ticket.status = "used"
    ticket.checked_in_at = datetime.utcnow()
    db.session.commit()

    return jsonify({
        "valid": True,
        "customer_name": ticket.holder_name,
        "event_name": ticket.event.name,
        "message": "Check-in thành công!"
    })

def payment_result():
    return """
        <h2>Thanh toán VNPAY</h2>
        <p>Đã quay trở lại website.</p>
        <a href="/">Về trang chủ</a>
    """