from sqlalchemy_serializer import SerializerMixin
from datetime import datetime



from ticketselling.ext.database import db


class User(db.Model, SerializerMixin):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(140))
    password = db.Column(db.String(512))
    email = db.Column(db.String(120),nullable = False)
    full_name = db.Column(db.String(150),nullable = False)
    role = db.Column(db.String(20))

class EventCategory(db.Model, SerializerMixin):
    __tablename__ = "event_categories"

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)

    def __repr__(self):
        return f"<EventCategory {self.name}"


class Event(db.Model, SerializerMixin):
    __tablename__ = "events"

    id = db.Column(db.Integer, primary_key=True)
    organizer_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    category_id = db.Column(db.Integer, db.ForeignKey("event_categories.id"))
    name = db.Column(db.String(255), nullable=False)
    banner = db.Column(db.String(255))
    description = db.Column(db.Text)
    location = db.Column(db.String(255))
    ticket_capacity = db.Column(db.Integer, default=0)
    ticket_price = db.Column(db.Integer, default=0)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)

    sale_start = db.Column(db.DateTime)
    sale_end = db.Column(db.DateTime)
    status = db.Column(db.String(20),default="ACTIVE")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    organizer = db.relationship("User",backref="organized_events")
    category = db.relationship("EventCategory",backref="events")

    tickets = db.relationship("Ticket", back_populates="event", lazy=True, cascade="all, delete-orphan")

    @property
    def tickets_sold(self):
        return len([t for t in self.tickets if t.status != "cancelled"])

    @property
    def total_revenue(self):
        return self.tickets_sold * (self.ticket_price or 0)

    @property
    def total_capacity(self):
        if self.ticket_types:
            return sum([t.max_quantity for t in self.ticket_types])
        return self.ticket_capacity

    def __repr__(self):
        return f"<Event {self.name}"

class Ticket(db.Model):
    __tablename__ = "tickets"

    id = db.Column(db.Integer, primary_key=True)
    ticket_code = db.Column(db.String(140), unique=True, nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey("events.id"), nullable=False)
    ticket_type_id = db.Column(db.Integer, db.ForeignKey("ticket_types.id"))
    price = db.Column(db.Numeric(12, 2), default=0)
    holder_name = db.Column(db.String(100), nullable=False)
    holder_email = db.Column(db.String(120), nullable=False)
    status = db.Column(db.String(20), default="valid")  # valid / used / cancelled
    checked_in_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    event = db.relationship("Event", back_populates="tickets")

    @staticmethod
    def generate_code():
        import uuid
        return uuid.uuid4().hex

    def __repr__(self):
        return f"<Ticket {self.ticket_code[:8]}...>"

class TicketType(db.Model, SerializerMixin):
    __tablename__ = "ticket_types"

    id = db.Column(db.Integer,primary_key=True)
    event_id = db.Column(db.Integer,db.ForeignKey("events.id"),nullable=False)
    name = db.Column(db.String(100),nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Numeric(12, 2),nullable=False)
    max_quantity = db.Column(db.Integer,nullable=False)

    current_stock = db.Column(db.Integer,nullable=False)

    event = db.relationship("Event",
                            backref=db.backref("ticket_types",
                                lazy=True,cascade="all, delete-orphan"))

    def __repr__(self):
        return f"<TicketType {self.name}>"

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