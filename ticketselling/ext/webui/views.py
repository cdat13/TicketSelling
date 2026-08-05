from flask import flash, render_template, request, redirect, url_for
from flask_simplelogin import login_required

from ticketselling.models import Event
from ticketselling.models import EventCategory

from ticketselling.ext.auth import create_user


from sqlalchemy import func

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

    # Kết quả tìm kiếm
    events = query.order_by(Event.start_time).all()

    # sự kiện nổi bật
    featured_events = (
        Event.query.filter(Event.status == "ACTIVE")
        .order_by(Event.id.asc())
        .limit(4)
        .all()
    )

    raw_locations = (
        Event.query.with_entities(Event.location)
        .filter(Event.location.isnot(None))
        .distinct()
        .all()
    )

    locations = sorted({
        item[0].split(",")[-1].strip()
        for item in raw_locations
        if item[0]
    })

    categories = EventCategory.query.order_by(
        EventCategory.name
    ).all()

    return render_template(
        "index.html",
        events=events,
        featured_events=featured_events,
        categories=categories,
        locations=locations,
        keyword=keyword,
        selected_location=location,
        selected_category=int(category) if category else None
    )


def event_list():

    keyword = request.args.get("keyword", "").strip()
    location = request.args.get("location", "")
    category = request.args.get("category", "")

    query = Event.query.filter(
        Event.status == "ACTIVE"
    )

    if keyword:
        query = query.filter(
            Event.name.ilike(f"%{keyword}%")
        )

    if location:
        query = query.filter(
            Event.location.ilike(f"%{location}")
        )

    if category:
        query = query.filter(
            Event.category_id == int(category)
        )

    events = (
        query.order_by(Event.start_time)
        .all()
    )

    locations = Event.query.with_entities(Event.location).distinct().all()

    locations = sorted(
        [x[0].strip() for x in locations]
    )

    categories = EventCategory.query.all()

    return render_template(
        "event/list.html",
        events=events,
        keyword=keyword,
        categories=categories,
        locations=locations,
        selected_location=location,
        selected_category=int(category) if category else None
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
        full_name = request.form.get("full_name", "").strip()
        email = request.form.get("email", "").strip().lower()
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        confirm = request.form.get("confirm", "")

        if not all([full_name, email, username, password, confirm, ]):
            err_msg = "Vui lòng nhập đầy đủ thông tin."

        elif "@" not in email:
            err_msg = "Địa chỉ email không hợp lệ."

        elif len(username) < 3:
            err_msg = "Tên đăng nhập phải có ít nhất 3 ký tự."

        elif len(password) < 6:
            err_msg = "Mật khẩu phải có ít nhất 6 ký tự."


        elif password != confirm:
            err_msg = "Mật khẩu xác nhận không khớp."


        else:
            try:
                create_user(
                    full_name=full_name,
                    email=email,
                    username=username,
                    password=password,
                )

                return redirect(
                    url_for("simplelogin.login")
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
    event = Event.query.filter_by(id = event_id, status = "ACTIVE").first()
    if event is None:
        flash("Sự kiện không tồn tại hoặc hiện không khả dụng.", "warning")
        return redirect(url_for("webui.index"))

    return render_template("event/detail.html", event=event)


def checkout():
    return render_template("checkout/checkout.html")
