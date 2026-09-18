import os
from datetime import datetime
from decimal import Decimal
from urllib.parse import parse_qs, urlsplit

import pytest
from flask import url_for
from werkzeug.security import check_password_hash, generate_password_hash

from ticketselling import create_app
from ticketselling.ext.database import db
from ticketselling.models import Event, EventCategory, TicketType, User


@pytest.fixture(scope="module")
def app():
    env_names = (
        "SQLALCHEMY_DATABASE_URI",
        "ENV_FOR_DYNACONF",
        "FORCE_ENV_FOR_DYNACONF",
    )
    old_env = {name: os.environ.get(name) for name in env_names}

    os.environ["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    os.environ["ENV_FOR_DYNACONF"] = "default"
    os.environ["FORCE_ENV_FOR_DYNACONF"] = "default"

    test_app = create_app(
        TESTING=True,
        WTF_CSRF_ENABLED=False,
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    with test_app.app_context():
        db.create_all()

    yield test_app

    with test_app.app_context():
        db.session.remove()
        db.drop_all()

    for name, value in old_env.items():
        if value is None:
            os.environ.pop(name, None)
        else:
            os.environ[name] = value


@pytest.fixture(autouse=True)
def reset_database(app):
    with app.app_context():
        db.session.remove()
        db.drop_all()
        db.create_all()

    yield

    with app.app_context():
        db.session.remove()


@pytest.fixture
def client(app):
    return app.test_client()


def login_url(app):
    with app.test_request_context():
        return url_for("simplelogin.login")


def add_user(
    *,
    username="testuser",
    password="MatKhau123",
    email="testuser@example.com",
    full_name="Nguyen Van Test",
):
    user = User(
        username=username,
        password=generate_password_hash(password),
        email=email,
        full_name=full_name,
        role="user",
    )
    db.session.add(user)
    db.session.commit()
    return user


def test_login_success(client, app):
    with app.app_context():
        add_user(username="alice", password="MatKhau123")

    response = client.post(
        login_url(app),
        data={"username": "alice", "password": "MatKhau123"},
        follow_redirects=False,
    )

    assert response.status_code == 302
    assert urlsplit(response.headers["Location"]).path == "/"

    with client.session_transaction() as session:
        assert session["simple_logged_in"] is True
        assert session["simple_username"] == "alice"


def test_login_rejects_wrong_password(client, app):
    with app.app_context():
        add_user(username="alice", password="MatKhau123")

    response = client.post(
        login_url(app),
        data={"username": "alice", "password": "sai-mat-khau"},
    )

    assert response.status_code == 401
    assert "Tên đăng nhập hoặc mật khẩu không đúng." in response.get_data(
        as_text=True
    )

    with client.session_transaction() as session:
        assert "simple_logged_in" not in session


def test_register_success(client, app):
    response = client.post(
        "/register",
        data={
            "full_name": "Tran Van An",
            "email": "an@example.com",
            "username": "tranvanan",
            "password": "MatKhau123",
            "confirm": "MatKhau123",
        },
        follow_redirects=False,
    )

    assert response.status_code == 302
    assert urlsplit(response.headers["Location"]).path == login_url(app)

    with app.app_context():
        saved_user = User.query.filter_by(username="tranvanan").one()
        assert saved_user.full_name == "Tran Van An"
        assert saved_user.email == "an@example.com"
        assert check_password_hash(saved_user.password, "MatKhau123")


def test_register_rejects_duplicate_username(client, app):
    with app.app_context():
        add_user(username="trungten", email="old@example.com")

    response = client.post(
        "/register",
        data={
            "full_name": "Nguoi Dang Ky Moi",
            "email": "new@example.com",
            "username": "trungten",
            "password": "MatKhau123",
            "confirm": "MatKhau123",
        },
    )

    assert response.status_code == 200
    assert "Tên đăng nhập đã tồn tại" in response.get_data(as_text=True)

    with app.app_context():
        assert User.query.filter_by(username="trungten").count() == 1


def test_event_detail_displays_event_and_ticket_information(client, app):
    with app.app_context():
        organizer = add_user(
            username="organizer",
            email="organizer@example.com",
            full_name="Ban To Chuc ABC",
        )
        category = EventCategory(name="Âm nhạc")
        event = Event(
            organizer=organizer,
            category=category,
            name="Dem Nhac Mua Thu",
            description="Chuong trinh am nhac dac biet.",
            location="Nha hat Thanh pho",
            start_time=datetime(2026, 10, 10, 19, 30),
            status="ACTIVE",
        )
        event.ticket_types.extend(
            [
                TicketType(
                    name="Standard",
                    price=Decimal("150000"),
                    max_quantity=100,
                    current_stock=50,
                ),
                TicketType(
                    name="VIP",
                    price=Decimal("300000"),
                    max_quantity=50,
                    current_stock=10,
                ),
                TicketType(
                    name="SVIP",
                    price=Decimal("500000"),
                    max_quantity=20,
                    current_stock=0,
                ),
            ]
        )
        db.session.add(event)
        db.session.commit()
        event_id = event.id

    response = client.get(f"/events/{event_id}")
    page = response.get_data(as_text=True)

    assert response.status_code == 200
    for expected_text in (
        "Dem Nhac Mua Thu",
        "Âm nhạc",
        "Ban To Chuc ABC",
        "10/10/2026",
        "19:30",
        "Nha hat Thanh pho",
        "Chuong trinh am nhac dac biet.",
        "Điều khoản &amp; Quy định",
        "Standard",
        "150.000đ",
        "VIP",
        "300.000đ",
        "SVIP",
        "500.000đ",
        "Còn vé",
        "Hết vé",
        "Đăng nhập để mua vé",
    ):
        assert expected_text in page


def test_inactive_event_is_not_available(client, app):
    with app.app_context():
        event = Event(
            name="Su kien nhap",
            start_time=datetime(2026, 11, 1, 8, 0),
            status="DRAFT",
        )
        db.session.add(event)
        db.session.commit()
        event_id = event.id

    response = client.get(f"/events/{event_id}", follow_redirects=False)

    assert response.status_code == 302
    assert urlsplit(response.headers["Location"]).path == "/"


def test_checkout_requires_login(client, app):
    response = client.get("/checkout", follow_redirects=False)

    assert response.status_code == 302
    redirect_url = urlsplit(response.headers["Location"])
    assert redirect_url.path == login_url(app)
    assert parse_qs(redirect_url.query)["next"] == ["/checkout"]