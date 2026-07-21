from sqlalchemy_serializer import SerializerMixin
from datetime import datetime


from ticketselling.ext.database import db


class User(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(140))
    password = db.Column(db.String(512))

class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)

    # Mã đơn hàng nội bộ
    order_code = db.Column(db.String(50), unique=True, nullable=False)

    # Thông tin khách hàng
    customer_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)

    # Thông tin đơn hàng
    total_amount = db.Column(db.Integer, nullable=False)

    ticket_quantity = db.Column(db.Integer, default=1)

    note = db.Column(db.Text)

    # Payment
    payment_method = db.Column(db.String(30))

    payment_status = db.Column(
        db.String(20),
        default="Pending"
    )
    # Pending
    # Paid
    # Failed
    # Cancelled

    # VNPAY
    vnp_txn_ref = db.Column(db.String(100))

    vnp_transaction_no = db.Column(db.String(100))

    vnp_bank_code = db.Column(db.String(30))

    vnp_response_code = db.Column(db.String(10))

    vnp_secure_hash = db.Column(db.String(255))

    paid_at = db.Column(db.DateTime)

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    def __repr__(self):
        return f"<Order {self.order_code}>"