from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app import db, login_manager


class Role:
    TOURIST = "tourist"
    ORGANIZER = "organizer"
    ADMIN = "admin"


class BookingStatus:
    PENDING = "pending"
    PAID = "paid"
    CANCELLED = "cancelled"


class PaymentStatus:
    PENDING = "pending"
    SUCCESS = "success"
    FAILED = "failed"


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    full_name = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20))
    role = db.Column(db.String(20), nullable=False, default=Role.TOURIST)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    activities = db.relationship("Activity", back_populates="organizer", lazy="dynamic")
    bookings = db.relationship("Booking", back_populates="tourist", lazy="dynamic")

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    @property
    def is_admin(self) -> bool:
        return self.role == Role.ADMIN

    @property
    def is_organizer(self) -> bool:
        return self.role == Role.ORGANIZER

    @property
    def is_tourist(self) -> bool:
        return self.role == Role.TOURIST


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    slug = db.Column(db.String(80), unique=True, nullable=False)

    activities = db.relationship("Activity", back_populates="category", lazy="dynamic")


class Activity(db.Model):
    __tablename__ = "activities"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False, default=60)
    image_url = db.Column(db.String(300))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False)
    organizer_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    category = db.relationship("Category", back_populates="activities")
    organizer = db.relationship("User", back_populates="activities")
    schedules = db.relationship(
        "Schedule", back_populates="activity", lazy="dynamic", cascade="all, delete-orphan"
    )

    @property
    def activity_type_label(self) -> str:
        return self.category.name if self.category else "Мероприятие"


class Schedule(db.Model):
    __tablename__ = "schedules"

    id = db.Column(db.Integer, primary_key=True)
    start_datetime = db.Column(db.DateTime, nullable=False, index=True)
    seats_total = db.Column(db.Integer, nullable=False)
    seats_booked = db.Column(db.Integer, nullable=False, default=0)

    activity_id = db.Column(db.Integer, db.ForeignKey("activities.id"), nullable=False)

    activity = db.relationship("Activity", back_populates="schedules")
    bookings = db.relationship("Booking", back_populates="schedule", lazy="dynamic")

    @property
    def seats_available(self) -> int:
        return max(0, self.seats_total - self.seats_booked)

    def can_book(self, seats: int) -> bool:
        return seats > 0 and self.seats_available >= seats


class Booking(db.Model):
    __tablename__ = "bookings"

    id = db.Column(db.Integer, primary_key=True)
    seats_count = db.Column(db.Integer, nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), nullable=False, default=BookingStatus.PENDING)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    schedule_id = db.Column(db.Integer, db.ForeignKey("schedules.id"), nullable=False)

    tourist = db.relationship("User", back_populates="bookings")
    schedule = db.relationship("Schedule", back_populates="bookings")
    payment = db.relationship("Payment", back_populates="booking", uselist=False)

    @property
    def status_label(self) -> str:
        labels = {
            BookingStatus.PENDING: "Ожидает оплаты",
            BookingStatus.PAID: "Оплачено",
            BookingStatus.CANCELLED: "Отменено",
        }
        return labels.get(self.status, self.status)


class Payment(db.Model):
    __tablename__ = "payments"

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), nullable=False, default=PaymentStatus.PENDING)
    card_last4 = db.Column(db.String(4))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    paid_at = db.Column(db.DateTime)

    booking_id = db.Column(db.Integer, db.ForeignKey("bookings.id"), unique=True, nullable=False)

    booking = db.relationship("Booking", back_populates="payment")
