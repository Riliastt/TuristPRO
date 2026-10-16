from datetime import datetime

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app import db
from app.models import Booking, BookingStatus, Payment, PaymentStatus, Schedule
from app.utils import tourist_required

booking_bp = Blueprint("booking", __name__, url_prefix="/booking")


@booking_bp.route("/<int:schedule_id>", methods=["GET", "POST"])
@login_required
@tourist_required
def book(schedule_id):
    schedule = Schedule.query.get_or_404(schedule_id)
    activity = schedule.activity

    if schedule.start_datetime < datetime.utcnow():
        flash("Нельзя забронировать прошедшее мероприятие.", "warning")
        return redirect(url_for("catalog.activity_detail", activity_id=activity.id))

    if request.method == "POST":
        seats_count = request.form.get("seats_count", type=int, default=1)

        if not schedule.can_book(seats_count):
            flash("Недостаточно свободных мест.", "danger")
            return redirect(url_for("booking.book", schedule_id=schedule_id))

        total_amount = activity.price * seats_count
        schedule.seats_booked += seats_count
        booking = Booking(
            user_id=current_user.id,
            schedule_id=schedule.id,
            seats_count=seats_count,
            total_amount=total_amount,
            status=BookingStatus.PENDING,
        )
        db.session.add(booking)
        db.session.flush()

        payment = Payment(
            booking_id=booking.id,
            amount=total_amount,
            status=PaymentStatus.PENDING,
        )
        db.session.add(payment)
        db.session.commit()

        return redirect(url_for("booking.payment", booking_id=booking.id))

    return render_template(
        "booking/book.html",
        schedule=schedule,
        activity=activity,
    )


@booking_bp.route("/payment/<int:booking_id>", methods=["GET", "POST"])
@login_required
@tourist_required
def payment(booking_id):
    booking = Booking.query.get_or_404(booking_id)

    if booking.user_id != current_user.id:
        flash("Доступ запрещён.", "danger")
        return redirect(url_for("tourist.dashboard"))

    if booking.status != BookingStatus.PENDING:
        flash("Это бронирование уже обработано.", "info")
        return redirect(url_for("tourist.booking_detail", booking_id=booking.id))

    if request.method == "POST":
        card_number = request.form.get("card_number", "").replace(" ", "")
        card_name = request.form.get("card_name", "").strip()
        card_expiry = request.form.get("card_expiry", "").strip()
        card_cvv = request.form.get("card_cvv", "").strip()

        if len(card_number) < 16 or not card_name or not card_expiry or len(card_cvv) < 3:
            flash("Заполните данные карты корректно.", "danger")
            return render_template("booking/payment.html", booking=booking)

        booking.status = BookingStatus.PAID
        booking.payment.status = PaymentStatus.SUCCESS
        booking.payment.card_last4 = card_number[-4:]
        booking.payment.paid_at = datetime.utcnow()
        db.session.commit()

        flash("Оплата прошла успешно! Бронирование подтверждено.", "success")
        return redirect(url_for("tourist.booking_detail", booking_id=booking.id))

    return render_template("booking/payment.html", booking=booking)


@booking_bp.route("/cancel/<int:booking_id>", methods=["POST"])
@login_required
@tourist_required
def cancel(booking_id):
    booking = Booking.query.get_or_404(booking_id)

    if booking.user_id != current_user.id:
        flash("Доступ запрещён.", "danger")
        return redirect(url_for("tourist.dashboard"))

    schedule = booking.schedule
    if booking.status in (BookingStatus.PENDING, BookingStatus.PAID):
        schedule.seats_booked = max(0, schedule.seats_booked - booking.seats_count)
        booking.status = BookingStatus.CANCELLED
        if booking.payment:
            booking.payment.status = PaymentStatus.FAILED
        db.session.commit()
        flash("Бронирование отменено. Места возвращены.", "info")
    else:
        flash("Бронирование уже отменено.", "warning")

    return redirect(url_for("tourist.dashboard"))
