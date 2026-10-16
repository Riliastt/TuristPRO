from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, logout_user

from app import db
from app.models import Role, User

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        full_name = request.form.get("full_name", "").strip()
        phone = request.form.get("phone", "").strip()
        password = request.form.get("password", "")
        password2 = request.form.get("password2", "")
        role = request.form.get("role", Role.TOURIST)

        if not email or not full_name or not password:
            flash("Заполните все обязательные поля.", "danger")
        elif password != password2:
            flash("Пароли не совпадают.", "danger")
        elif len(password) < 6:
            flash("Пароль должен быть не менее 6 символов.", "danger")
        elif User.query.filter_by(email=email).first():
            flash("Пользователь с таким email уже существует.", "danger")
        elif role not in (Role.TOURIST, Role.ORGANIZER):
            flash("Недопустимая роль при регистрации.", "danger")
        else:
            user = User(email=email, full_name=full_name, phone=phone, role=role)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            flash("Регистрация успешна. Войдите в систему.", "success")
            return redirect(url_for("auth.login"))

    return render_template("auth/register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return _redirect_by_role()

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        remember = bool(request.form.get("remember"))

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user, remember=remember)
            flash(f"Добро пожаловать, {user.full_name}!", "success")
            next_page = request.args.get("next")
            if next_page:
                return redirect(next_page)
            return _redirect_by_role()

        flash("Неверный email или пароль.", "danger")

    return render_template("auth/login.html")


@auth_bp.route("/logout")
def logout():
    logout_user()
    flash("Вы вышли из системы.", "info")
    return redirect(url_for("main.index"))


def _redirect_by_role():
    if current_user.is_admin:
        return redirect(url_for("admin.dashboard"))
    if current_user.is_organizer:
        return redirect(url_for("organizer.dashboard"))
    return redirect(url_for("tourist.dashboard"))
