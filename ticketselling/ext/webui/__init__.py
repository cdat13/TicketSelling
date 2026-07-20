from flask import Blueprint

from .views import index, only_admin, secret, login, register, checkout


bp = Blueprint(
    "webui",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/webui/static"
)



bp.add_url_rule("/login",view_func=login,endpoint="login")
bp.add_url_rule("/register",view_func=register,endpoint="register")

#trang chu
bp.add_url_rule("/", view_func=index)
bp.add_url_rule("/index", view_func=index)

#thanh toan
bp.add_url_rule("/checkout",view_func=checkout,endpoint="checkout")



bp.add_url_rule("/secret", view_func=secret, endpoint="secret")
bp.add_url_rule("/only_admin", view_func=only_admin, endpoint="onlyadmin")


def init_app(app):
    app.register_blueprint(bp)