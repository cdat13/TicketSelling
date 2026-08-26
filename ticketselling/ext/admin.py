from flask_admin import Admin
from flask_admin.base import AdminIndexView
from flask_admin.contrib import sqla
from werkzeug.security import generate_password_hash
from flask import redirect, url_for, session
from ticketselling.ext.database import db

# Proteck admin with login / Monkey Patch

def is_admin_logged_in():
    if 'simplelogin' not in session:
        return False

    username = session.get('simplelogin')
    from ticketselling.models import User
    user = User.query.filter_by(username=username).first()

    return user is not None and user.role == 'admin'

class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return is_admin_logged_in()

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('webui.index'))

class ProtectedModelView(sqla.ModelView):
    def is_accessible(self):
        return is_admin_logged_in()

class UserAdmin(ProtectedModelView):
    column_list = ["username", "email", "role", "status"]
    can_edit = True

    def on_model_change(self, form, model, is_created):
        model.password = generate_password_hash(model.password)

class EventAdmin(ProtectedModelView):
    column_list = ('id', 'name', 'location', 'start_time', 'status')
    column_searchable_list = ['name']
    column_filters = ['status']
    column_editable_list = ['status']
    column_labels = dict(
        name='Tên sự kiện',
        location='Địa điểm',
        start_time='Thời gian',
        status='Trạng thái'
    )


def init_app(app):
    admin = Admin(
        name="Quản trị Hệ thống",
        index_view=MyAdminIndexView(endpoint="system_admin", url="/system-admin"),
        endpoint = "system_admin",
        url = "/system-admin"
    )
    from ticketselling.models import User, Event

    admin.add_view(UserAdmin(User, db.session, name="Người dùng"))
    admin.add_view(EventAdmin(Event, db.session, name="Sự kiện"))

    admin.init_app(app)

