from functools import wraps

from flask import abort, flash, redirect, url_for
from flask_login import current_user

from app.models import Role


def role_required(*roles):
    def decorator(view):
        @wraps(view)
        def wrapped(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(url_for("auth.login"))
            if current_user.role not in roles:
                flash("У вас нет доступа к этой странице.", "danger")
                abort(403)
            return view(*args, **kwargs)

        return wrapped

    return decorator


def admin_required(view):
    return role_required(Role.ADMIN)(view)


def organizer_required(view):
    return role_required(Role.ORGANIZER, Role.ADMIN)(view)


def tourist_required(view):
    return role_required(Role.TOURIST)(view)
