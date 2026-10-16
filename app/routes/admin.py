from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required

from app import db
from app.models import Activity, Booking, Category, Role, User
from app.utils import admin_required

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.route("/dashboard")
@login_required
@admin_required
def dashboard():
    stats = {
        "users": User.query.count(),
        "activities": Activity.query.count(),
        "bookings": Booking.query.count(),
        "categories": Category.query.count(),
    }
    recent_bookings = Booking.query.order_by(Booking.created_at.desc()).limit(10).all()
    return render_template("admin/dashboard.html", stats=stats, recent_bookings=recent_bookings)


@admin_bp.route("/users")
@login_required
@admin_required
def users():
    all_users = User.query.order_by(User.created_at.desc()).all()
    return render_template("admin/users.html", users=all_users)


@admin_bp.route("/users/<int:user_id>/role", methods=["POST"])
@login_required
@admin_required
def change_role(user_id):
    user = User.query.get_or_404(user_id)
    new_role = request.form.get("role")
    if new_role in (Role.TOURIST, Role.ORGANIZER, Role.ADMIN):
        user.role = new_role
        db.session.commit()
        flash(f"Роль пользователя {user.full_name} изменена.", "success")
    return redirect(url_for("admin.users"))


@admin_bp.route("/categories", methods=["GET", "POST"])
@login_required
@admin_required
def categories():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        slug = request.form.get("slug", "").strip().lower()
        if name and slug:
            if Category.query.filter((Category.name == name) | (Category.slug == slug)).first():
                flash("Категория с таким именем или slug уже существует.", "danger")
            else:
                db.session.add(Category(name=name, slug=slug))
                db.session.commit()
                flash("Категория добавлена.", "success")
        else:
            flash("Укажите название и slug.", "danger")
        return redirect(url_for("admin.categories"))

    all_categories = Category.query.order_by(Category.name).all()
    return render_template("admin/categories.html", categories=all_categories)


@admin_bp.route("/activities")
@login_required
@admin_required
def activities():
    all_activities = Activity.query.order_by(Activity.created_at.desc()).all()
    return render_template("admin/activities.html", activities=all_activities)


@admin_bp.route("/activities/<int:activity_id>/toggle", methods=["POST"])
@login_required
@admin_required
def toggle_activity(activity_id):
    activity = Activity.query.get_or_404(activity_id)
    activity.is_active = not activity.is_active
    db.session.commit()
    flash("Статус мероприятия изменён.", "success")
    return redirect(url_for("admin.activities"))


@admin_bp.route("/bookings")
@login_required
@admin_required
def bookings():
    all_bookings = Booking.query.order_by(Booking.created_at.desc()).all()
    return render_template("admin/bookings.html", bookings=all_bookings)
