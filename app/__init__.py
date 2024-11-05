# app/__init__.py

from flask import Flask
from modules.database.db import db
from flask_migrate import Migrate
from flask_login import LoginManager
from app.views.main import bp as main_bp
from app.views.auth import bp as auth_bp
from app.views.accounts import bp as accounts_bp
from app.views.transactions import bp as transactions_bp

def create_app(config_object='config.DevelopmentConfig'):
    app = Flask(__name__)
    app.config.from_object(config_object)

    # Initialize extensions
    db.init_app(app)
    migrate = Migrate(app, db)

    # Initialize Flask-Login
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        from modules.models.user import User
        return User.query.get(int(user_id))

    # Register Blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(accounts_bp)
    app.register_blueprint(transactions_bp)

    return app
