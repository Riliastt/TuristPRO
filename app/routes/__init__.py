from app.routes.admin import admin_bp
from app.routes.auth import auth_bp
from app.routes.booking import booking_bp
from app.routes.catalog import catalog_bp
from app.routes.main import main_bp
from app.routes.organizer import organizer_bp
from app.routes.tourist import tourist_bp


def register_blueprints(app):
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(catalog_bp)
    app.register_blueprint(booking_bp)
    app.register_blueprint(tourist_bp)
    app.register_blueprint(organizer_bp)
    app.register_blueprint(admin_bp)
