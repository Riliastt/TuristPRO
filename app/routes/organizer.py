from datetime import datetime

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app import db
from app.models import Activity, Booking, Category, Schedule
from app.utils import organizer_required

organizer_bp = Blueprint("organizer", __name__, url_prefix="/organizer")


@organizer_bp.route("/dashboard")
@login_required
@organizer_required
def dashboard():
    activities = _organizer_activities().order_by(Activity.created_at.desc()).all()
    return render_template("organizer/dashboard.html", activities=activities)


@organizer_bp.route("/activities/new", methods=["GET", "POST"])
@login_required
@organizer_required
def activity_new():
    categories = Category.query.order_by(Category.name).all()

    if request.method == "POST":
        activity = _build_activity_from_form()
        if activity:
            db.session.add(activity)
            db.session.commit()
            flash("Мероприятие создано.", "success")
            return redirect(url_for("organizer.activity_edit", activity_id=activity.id))

    return render_template("organizer/activity_form.html", categories=categories, activity=None)


@organizer_bp.route("/activities/<int:activity_id>/edit", methods=["GET", "POST"])
@login_required
@organizer_required
def activity_edit(activity_id):
    activity = _get_own_activity(activity_id)
    categories = Category.query.order_by(Category.name).all()

    if request.method == "POST":
        updated = _build_activity_from_form(existing=activity)
        if updated:
            db.session.commit()
            flash("Мероприятие обновлено.", "success")
            return redirect(url_for("organizer.dashboard"))

    schedules = (
        Schedule.query.filter_by(activity_id=activity.id)
        .order_by(Schedule.start_datetime)
        .all()
    )
    bookings = (
        Booking.query.join(Schedule)
        .filter(Schedule.activity_id == activity.id)
        .order_by(Booking.created_at.desc())
        .all()
    )

    return render_template(
        "organizer/activity_form.html",
        categories=categories,
        activity=activity,
        schedules=schedules,
        bookings=bookings,
    )


@organizer_bp.route("/activities/<int:activity_id>/schedule", methods=["POST"])
@login_required
@organizer_required
def schedule_add(activity_id):
    activity = _get_own_activity(activity_id)

    date_str = request.form.get("date", "")
    time_str = request.form.get("time", "")
    seats_total = request.form.get("seats_total", type=int)

    try:
        start_datetime = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
    except ValueError:
        flash("Укажите корректную дату и время.", "danger")
        return redirect(url_for("organizer.activity_edit", activity_id=activity.id))

    if not seats_total or seats_total < 1:
        flash("Количество мест должно быть больше 0.", "danger")
        return redirect(url_for("organizer.activity_edit", activity_id=activity.id))

    schedule = Schedule(
        activity_id=activity.id,
        start_datetime=start_datetime,
        seats_total=seats_total,
        seats_booked=0,
    )
    db.session.add(schedule)
    db.session.commit()
    flash("Слот расписания добавлен.", "success")
    return redirect(url_for("organizer.activity_edit", activity_id=activity.id))


@organizer_bp.route("/schedule/<int:schedule_id>/delete", methods=["POST"])
@login_required
@organizer_required
def schedule_delete(schedule_id):
    schedule = Schedule.query.get_or_404(schedule_id)
    _get_own_activity(schedule.activity_id)

    if schedule.seats_booked > 0:
        flash("Нельзя удалить слот с активными бронированиями.", "danger")
    else:
        db.session.delete(schedule)
        db.session.commit()
        flash("Слот удалён.", "info")

    return redirect(url_for("organizer.activity_edit", activity_id=schedule.activity_id))


def _organizer_activities():
    if current_user.is_admin:
        return Activity.query
    return Activity.query.filter_by(organizer_id=current_user.id)


def _get_own_activity(activity_id):
    activity = Activity.query.get_or_404(activity_id)
    if not current_user.is_admin and activity.organizer_id != current_user.id:
        from flask import abort

        abort(403)
    return activity


def _build_activity_from_form(existing=None):
    title = request.form.get("title", "").strip()
    description = request.form.get("description", "").strip()
    location = request.form.get("location", "").strip()
    price = request.form.get("price", type=float)
    duration_minutes = request.form.get("duration_minutes", type=int, default=60)
    category_id = request.form.get("category_id", type=int)
    image_url = request.form.get("image_url", "").strip() or None
    is_active = bool(request.form.get("is_active"))

    if not title or not description or not location or price is None or not category_id:
        flash("Заполните все обязательные поля мероприятия.", "danger")
        return None

    if existing:
        activity = existing
    else:
        activity = Activity(organizer_id=current_user.id)

    activity.title = title
    activity.description = description
    activity.location = location
    activity.price = price
    activity.duration_minutes = duration_minutes or 60
    activity.category_id = category_id
    activity.image_url = image_url
    activity.is_active = is_active

    return activity
