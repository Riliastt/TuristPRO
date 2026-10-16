from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()


def create_app(config_class=None):
    from config import Config

    app = Flask(__name__)
    app.config.from_object(config_class or Config)

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    login_manager.login_view = "auth.login"
    login_manager.login_message = "Войдите в систему для доступа к этой странице."
    login_manager.login_message_category = "warning"

    from app.routes import register_blueprints

    register_blueprints(app)

    with app.app_context():
        from app import models  # noqa: F401

        db.create_all()

    return app
