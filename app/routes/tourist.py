from flask import Blueprint, render_template
from flask_login import current_user, login_required

from app.models import Booking
from app.utils import tourist_required

tourist_bp = Blueprint("tourist", __name__, url_prefix="/tourist")


@tourist_bp.route("/dashboard")
@login_required
@tourist_required
def dashboard():
    bookings = (
        Booking.query.filter_by(user_id=current_user.id)
        .order_by(Booking.created_at.desc())
        .all()
    )
    return render_template("tourist/dashboard.html", bookings=bookings)


@tourist_bp.route("/booking/<int:booking_id>")
@login_required
@tourist_required
def booking_detail(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    if booking.user_id != current_user.id:
        from flask import abort

        abort(403)
    return render_template("tourist/booking_detail.html", booking=booking)
