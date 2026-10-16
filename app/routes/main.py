from datetime import datetime

from flask import Blueprint, render_template
from app.models import Activity, Booking, BookingStatus, Schedule

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    popular = (
        Activity.query.filter_by(is_active=True)
        .order_by(Activity.created_at.desc())
        .limit(6)
        .all()
    )
    upcoming_count = (
        Schedule.query.filter(Schedule.start_datetime >= datetime.utcnow()).count()
    )
    paid_bookings = Booking.query.filter_by(status=BookingStatus.PAID).count()
    return render_template(
        "index.html",
        popular=popular,
        upcoming_count=upcoming_count,
        paid_bookings=paid_bookings,
    )
