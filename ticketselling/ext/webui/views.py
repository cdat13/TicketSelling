from flask import render_template
from flask_simplelogin import login_required


def index():
    return render_template("index.html")


@login_required
def secret():
    return "This can be seen only if user is logged in"


@login_required(username="admin")
def only_admin():
    return "only admin user can see this text"


def login():
    return render_template("auth/login.html")


def register():
    return render_template("auth/register.html")

    
def checkout():
    return render_template("checkout/checkout.html")