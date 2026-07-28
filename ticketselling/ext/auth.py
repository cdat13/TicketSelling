from flask_simplelogin import SimpleLogin, Message
from pyexpat.errors import messages
from werkzeug.security import check_password_hash, generate_password_hash

from ticketselling.ext.database import db
from ticketselling.models import User


def verify_login(user):
    """Validates user login"""
    username = user.get("username")
    password = user.get("password")
    if not username or not password:
        return False
    existing_user = User.query.filter_by(username=username).first()
    if not existing_user:
        return False
    if check_password_hash(existing_user.password, password):
        return True
    return False


def create_user(full_name, email,username, password):
    """Creates a new user"""
    existing_username = User.query.filter_by(
        username=username
    ).first()
    if existing_username:
        raise RuntimeError("Tên đăng nhập đã tồn tại")
    existing_email = User.query.filter_by(
        email=email
    ).first()

    if existing_email:
        raise RuntimeError(
            "Email đã được sử dụng."
        )

    user = User(full_name=full_name,email=email,username=username, password=generate_password_hash(password))
    try:
        db.session.add(user)
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise

    return user


def init_app(app):
    messages = {
        "login_success": Message("Đăng nhập thành công.", "success"),
        "login_failure": Message("Tên đăng nhập hoặc mật khẩu không đúng.", "danger"),
        "login_required": Message("Bạn cần đăng nhập trước.", "warning"),
        "logout": Message("Đăng xuất thành công.", "success"),
        "auth_error": Message("Lỗi xác thực {0}.", "danger"),

    }
    SimpleLogin(app, login_checker=verify_login, messages=messages)
