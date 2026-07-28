from datetime import datetime

from werkzeug.security import generate_password_hash

from ticketselling.ext.database import db
from ticketselling.models import Event, EventCategory, TicketType, User


USERS = [
    {
        "username": "admin",
        "email": "admin@ticketselling.local",
        "full_name": "Quản trị viên",
        "password": "Admin@123",
    },
    {
        "username": "organizer_music",
        "email": "music@ticketselling.local",
        "full_name": "VietMusic Entertainment",
        "password": "123456",
    },
    {
        "username": "organizer_event",
        "email": "event@ticketselling.local",
        "full_name": "VietEvent Corporation",
        "password": "123456",
    },
    {
        "username": "organizer_sport",
        "email": "sport@ticketselling.local",
        "full_name": "Vietnam Sport Center",
        "password": "123456",
    },
    {
        "username": "customer_test",
        "email": "customer@ticketselling.local",
        "full_name": "Khách hàng thử nghiệm",
        "password": "123456",
    },
]

CATEGORIES = [
    "Âm nhạc",
    "Hội thảo",
    "Thể thao",
    "Sân khấu",
    "Công nghệ",
]

EVENTS = [
    {
        "name": "Summer Music Festival 2026",
        "organizer": "organizer_music",
        "category": "Âm nhạc",
        "banner": "img/demo.png",
        "description": (
            "Đêm nhạc mùa hè quy tụ nhiều nghệ sĩ trẻ và các ban nhạc nổi bật. "
            "Chương trình mang đến không gian âm nhạc ngoài trời với nhiều thể loại "
            "như pop, rock, EDM và ballad.\n\n"
            "Khán giả nên có mặt trước giờ bắt đầu ít nhất 30 phút để hoàn tất "
            "thủ tục check-in."
        ),
        "location": "Nhà thi đấu Phú Thọ, TP. Hồ Chí Minh",
        "start_time": datetime(2026, 8, 15, 18, 0),
        "end_time": datetime(2026, 8, 15, 23, 0),
        "sale_start": datetime(2026, 7, 20, 8, 0),
        "sale_end": datetime(2026, 8, 15, 16, 0),
        "status": "ACTIVE",
        "ticket_types": [
            {"name": "Standard", "description": "Khu vực tiêu chuẩn", "price": 500000, "max_quantity": 6, "current_stock": 120},
            {"name": "VIP", "description": "Khu vực gần sân khấu", "price": 1320000, "max_quantity": 4, "current_stock": 40},
            {"name": "SVIP", "description": "Khu vực đặc biệt", "price": 2600000, "max_quantity": 2, "current_stock": 0},
        ],
    },
    {
        "name": "Vietnam Digital Business Forum 2026",
        "organizer": "organizer_event",
        "category": "Hội thảo",
        "banner": "img/demo.png",
        "description": (
            "Diễn đàn dành cho sinh viên, doanh nghiệp và những người quan tâm đến "
            "chuyển đổi số, thương mại điện tử và quản trị dự án.\n\n"
            "Chương trình gồm các phiên chia sẻ, hỏi đáp và kết nối với diễn giả."
        ),
        "location": "Trung tâm Hội nghị 272, TP. Hồ Chí Minh",
        "start_time": datetime(2026, 8, 28, 8, 0),
        "end_time": datetime(2026, 8, 28, 17, 0),
        "sale_start": datetime(2026, 7, 25, 8, 0),
        "sale_end": datetime(2026, 8, 27, 23, 0),
        "status": "ACTIVE",
        "ticket_types": [
            {"name": "Sinh viên", "description": "Yêu cầu thẻ sinh viên", "price": 150000, "max_quantity": 1, "current_stock": 150},
            {"name": "Tiêu chuẩn", "description": "Vé tham dự hội thảo", "price": 350000, "max_quantity": 5, "current_stock": 80},
            {"name": "Doanh nghiệp", "description": "Khu vực networking", "price": 750000, "max_quantity": 5, "current_stock": 30},
        ],
    },
    {
        "name": "Giải chạy Thành phố Xanh 2026",
        "organizer": "organizer_sport",
        "category": "Thể thao",
        "banner": "img/demo.png",
        "description": (
            "Giải chạy cộng đồng hướng đến lối sống lành mạnh và bảo vệ môi trường. "
            "Người tham dự có thể lựa chọn cự ly phù hợp với thể lực.\n\n"
            "Bộ vật phẩm bao gồm áo chạy, số báo danh và huy chương hoàn thành."
        ),
        "location": "Khu đô thị Sala, TP. Hồ Chí Minh",
        "start_time": datetime(2026, 9, 6, 5, 0),
        "end_time": datetime(2026, 9, 6, 10, 0),
        "sale_start": datetime(2026, 7, 25, 8, 0),
        "sale_end": datetime(2026, 9, 1, 23, 0),
        "status": "ACTIVE",
        "ticket_types": [
            {"name": "5 KM", "description": "Cự ly phong trào", "price": 250000, "max_quantity": 3, "current_stock": 300},
            {"name": "10 KM", "description": "Cự ly nâng cao", "price": 400000, "max_quantity": 3, "current_stock": 200},
            {"name": "21 KM", "description": "Cự ly bán marathon", "price": 650000, "max_quantity": 2, "current_stock": 100},
        ],
    },
    {
        "name": "Kịch nói Chuyến Tàu Ký Ức",
        "organizer": "organizer_event",
        "category": "Sân khấu",
        "banner": "img/demo.png",
        "description": (
            "Vở kịch kể về hành trình gặp lại những ký ức cũ của một gia đình sau "
            "nhiều năm xa cách. Nội dung gần gũi, phù hợp với khán giả trưởng thành."
        ),
        "location": "Nhà hát Thành phố, TP. Hồ Chí Minh",
        "start_time": datetime(2026, 9, 12, 19, 30),
        "end_time": datetime(2026, 9, 12, 21, 30),
        "sale_start": datetime(2026, 8, 1, 8, 0),
        "sale_end": datetime(2026, 9, 12, 18, 0),
        "status": "ACTIVE",
        "ticket_types": [
            {"name": "Hạng C", "description": "Khu vực phía sau", "price": 300000, "max_quantity": 6, "current_stock": 90},
            {"name": "Hạng B", "description": "Khu vực trung tâm", "price": 500000, "max_quantity": 6, "current_stock": 60},
            {"name": "Hạng A", "description": "Khu vực gần sân khấu", "price": 800000, "max_quantity": 4, "current_stock": 25},
        ],
    },
    {
        "name": "AI for Developers Workshop",
        "organizer": "organizer_event",
        "category": "Công nghệ",
        "banner": "img/demo.png",
        "description": (
            "Workshop thực hành dành cho sinh viên và lập trình viên mới bắt đầu "
            "tìm hiểu cách tích hợp trí tuệ nhân tạo vào ứng dụng.\n\n"
            "Người tham dự nên mang theo laptop để thực hành."
        ),
        "location": "Đại học Mở TP. Hồ Chí Minh",
        "start_time": datetime(2026, 9, 20, 8, 30),
        "end_time": datetime(2026, 9, 20, 16, 30),
        "sale_start": datetime(2026, 8, 10, 8, 0),
        "sale_end": datetime(2026, 9, 19, 23, 0),
        "status": "ACTIVE",
        "ticket_types": [
            {"name": "Sinh viên", "description": "Vé dành cho sinh viên", "price": 100000, "max_quantity": 1, "current_stock": 80},
            {"name": "Tiêu chuẩn", "description": "Vé tham gia workshop", "price": 300000, "max_quantity": 3, "current_stock": 50},
        ],
    },
    {
        "name": "Acoustic Night: Những Ngày Mưa",
        "organizer": "organizer_music",
        "category": "Âm nhạc",
        "banner": "img/demo.png",
        "description": (
            "Đêm nhạc acoustic với không gian nhỏ, gần gũi và những ca khúc nhẹ nhàng. "
            "Số lượng vé giới hạn để bảo đảm trải nghiệm của khán giả."
        ),
        "location": "Nhà Văn hóa Thanh Niên, TP. Hồ Chí Minh",
        "start_time": datetime(2026, 10, 3, 19, 0),
        "end_time": datetime(2026, 10, 3, 22, 0),
        "sale_start": datetime(2026, 8, 20, 8, 0),
        "sale_end": datetime(2026, 10, 3, 17, 0),
        "status": "ACTIVE",
        "ticket_types": [
            {"name": "Vé thường", "description": "Ghế ngồi tiêu chuẩn", "price": 350000, "max_quantity": 4, "current_stock": 70},
            {"name": "Vé đôi", "description": "Hai ghế liền nhau", "price": 650000, "max_quantity": 2, "current_stock": 20},
        ],
    },
    {
        "name": "Saigon Basketball All-Star 2026",
        "organizer": "organizer_sport",
        "category": "Thể thao",
        "banner": "img/demo.png",
        "description": (
            "Trận đấu giao hữu quy tụ các vận động viên bóng rổ nổi bật. "
            "Chương trình có phần giao lưu và biểu diễn trong giờ nghỉ."
        ),
        "location": "Nhà thi đấu Hồ Xuân Hương, TP. Hồ Chí Minh",
        "start_time": datetime(2026, 10, 18, 18, 30),
        "end_time": datetime(2026, 10, 18, 21, 30),
        "sale_start": datetime(2026, 9, 1, 8, 0),
        "sale_end": datetime(2026, 10, 18, 16, 0),
        "status": "ACTIVE",
        "ticket_types": [
            {"name": "Khán đài", "description": "Ghế khán đài", "price": 200000, "max_quantity": 6, "current_stock": 200},
            {"name": "Cận sân", "description": "Khu vực gần sân thi đấu", "price": 550000, "max_quantity": 4, "current_stock": 50},
            {"name": "Courtside", "description": "Hàng ghế sát sân", "price": 1200000, "max_quantity": 2, "current_stock": 12},
        ],
    },
    {
        "name": "Tech Career Day 2026",
        "organizer": "organizer_event",
        "category": "Công nghệ",
        "banner": "img/demo.png",
        "description": (
            "Ngày hội nghề nghiệp dành cho sinh viên công nghệ thông tin. "
            "Người tham dự có thể gặp gỡ doanh nghiệp, nghe chia sẻ nghề nghiệp "
            "và tham gia phỏng vấn thử."
        ),
        "location": "Nhà Văn hóa Sinh viên, TP. Hồ Chí Minh",
        "start_time": datetime(2026, 11, 7, 8, 0),
        "end_time": datetime(2026, 11, 7, 17, 0),
        "sale_start": datetime(2026, 9, 15, 8, 0),
        "sale_end": datetime(2026, 11, 6, 23, 0),
        "status": "ACTIVE",
        "ticket_types": [
            {"name": "Miễn phí", "description": "Vé tham dự cơ bản", "price": 0, "max_quantity": 1, "current_stock": 500},
            {"name": "CV Review", "description": "Bao gồm một lượt góp ý CV", "price": 100000, "max_quantity": 1, "current_stock": 80},
        ],
    },
]


def _seed_users():
    users = {}

    for item in USERS:
        user = User.query.filter_by(username=item["username"]).first()

        if user is None:
            user = User(
                username=item["username"],
                email=item["email"],
                full_name=item["full_name"],
                password=generate_password_hash(item["password"]),
            )
            db.session.add(user)
        else:
            user.email = item["email"]
            user.full_name = item["full_name"]

        users[item["username"]] = user

    db.session.flush()
    return users


def _seed_categories():
    categories = {}

    for name in CATEGORIES:
        category = EventCategory.query.filter_by(name=name).first()

        if category is None:
            category = EventCategory(name=name)
            db.session.add(category)

        categories[name] = category

    db.session.flush()
    return categories


def _seed_events(users, categories):
    event_count = 0
    ticket_count = 0

    for item in EVENTS:
        event = Event.query.filter_by(name=item["name"]).first()

        if event is None:
            event = Event(name=item["name"])
            db.session.add(event)

        event.organizer = users[item["organizer"]]
        event.category = categories[item["category"]]
        event.banner = item["banner"]
        event.description = item["description"]
        event.location = item["location"]
        event.start_time = item["start_time"]
        event.end_time = item["end_time"]
        event.sale_start = item["sale_start"]
        event.sale_end = item["sale_end"]
        event.status = item["status"]

        db.session.flush()
        event_count += 1

        for ticket_data in item["ticket_types"]:
            ticket = TicketType.query.filter_by(
                event_id=event.id,
                name=ticket_data["name"],
            ).first()

            if ticket is None:
                ticket = TicketType(
                    event=event,
                    name=ticket_data["name"],
                )
                db.session.add(ticket)

            ticket.description = ticket_data["description"]
            ticket.price = ticket_data["price"]
            ticket.max_quantity = ticket_data["max_quantity"]
            ticket.current_stock = ticket_data["current_stock"]
            ticket_count += 1

    return event_count, ticket_count


def seed_data():
    """Thêm hoặc cập nhật dữ liệu phát triển, không xóa dữ liệu đang có."""
    try:
        users = _seed_users()
        categories = _seed_categories()
        event_count, ticket_count = _seed_events(users, categories)
        db.session.commit()

        print("Tạo dữ liệu mẫu thành công.")
        print(f"- Người dùng: {len(USERS)}")
        print(f"- Danh mục: {len(CATEGORIES)}")
        print(f"- Sự kiện: {event_count}")
        print(f"- Loại vé: {ticket_count}")
        print("")
        print("Tài khoản thử:")
        print("- admin / Admin@123")
        print("- customer_test / 123456")
    except Exception:
        db.session.rollback()
        raise
