# app/__init__.py

from flask import Flask
from modules.database.db import db
from modules.services import ma  # Marshmallow instance
from flask_migrate import Migrate
from flask_login import LoginManager
from app.views.main import bp as main_bp
from app.views.auth import bp as auth_bp
from app.views.accounts import bp as accounts_bp
from app.views.transactions import bp as transactions_bp
from app.api import api_bp  # Import the API blueprint
from flask import make_response, jsonify, request, redirect, url_for

def create_app(config_object='config.DevelopmentConfig'):
    app = Flask(__name__)
    app.config.from_object(config_object)

    # Initialize extensions
    db.init_app(app)
    ma.init_app(app)  # Initialize Marshmallow
    migrate = Migrate(app, db)

    # Initialize Flask-Login
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        from modules.models.user import User
        return User.query.get(int(user_id))

    @login_manager.unauthorized_handler
    def unauthorized():
        if request.path.startswith('/api/'):
            return make_response(jsonify({'message': 'Unauthorized access'}), 401)
        else:
            return redirect(url_for('auth.login', next=request.url))

    # Register Blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(accounts_bp)
    app.register_blueprint(transactions_bp)
    app.register_blueprint(api_bp)  # Register the API blueprint

    return app

