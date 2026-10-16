from datetime import datetime

from flask import Blueprint, abort, render_template, request

from app.models import Activity, Category, Schedule

catalog_bp = Blueprint("catalog", __name__)


@catalog_bp.route("/catalog")
def catalog():
    query = Activity.query.filter_by(is_active=True)

    search = request.args.get("q", "").strip()
    category_id = request.args.get("category", type=int)
    min_price = request.args.get("min_price", type=float)
    max_price = request.args.get("max_price", type=float)

    if search:
        query = query.filter(
            Activity.title.ilike(f"%{search}%") | Activity.description.ilike(f"%{search}%")
        )
    if category_id:
        query = query.filter_by(category_id=category_id)
    if min_price is not None:
        query = query.filter(Activity.price >= min_price)
    if max_price is not None:
        query = query.filter(Activity.price <= max_price)

    activities = query.order_by(Activity.title).all()
    categories = Category.query.order_by(Category.name).all()

    return render_template(
        "catalog.html",
        activities=activities,
        categories=categories,
        search=search,
        category_id=category_id,
        min_price=min_price,
        max_price=max_price,
    )


@catalog_bp.route("/activity/<int:activity_id>")
def activity_detail(activity_id):
    activity = Activity.query.get_or_404(activity_id)
    if not activity.is_active and not (
        request.args.get("preview") == "1"
    ):
        abort(404)

    schedules = (
        Schedule.query.filter_by(activity_id=activity.id)
        .filter(Schedule.start_datetime >= datetime.utcnow())
        .order_by(Schedule.start_datetime)
        .all()
    )

    return render_template("activity_detail.html", activity=activity, schedules=schedules)
