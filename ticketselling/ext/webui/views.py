from math import expm1

from flask import render_template, request, redirect,url_for
from flask_simplelogin import login_required

from ticketselling.ext.auth import create_user


def index():
    return render_template("index.html")


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

        if not all([full_name,email,username,password,confirm,]):
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


def checkout():
    return render_template("checkout/checkout.html")