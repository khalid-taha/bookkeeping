# app/api/auth_api.py

from flask import request
from modules.models.user import User
from modules.database.db import db
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from flask_restx import Namespace, Resource, fields
from . import api

auth_ns = Namespace('auth', description='Authentication related operations')

login_model = auth_ns.model('Login', {
    'username': fields.String(required=True, description='Username'),
    'password': fields.String(required=True, description='Password')
})

user_model = auth_ns.model('User', {
    'id': fields.Integer(readOnly=True, description='User ID'),
    'username': fields.String(required=True, description='Username'),
    'role': fields.String(required=True, description='User role')
})

@auth_ns.route('/login')
class Login(Resource):
    @auth_ns.expect(login_model, validate=True)
    @auth_ns.marshal_with(user_model)
    def post(self):
        """Authenticate a user and log them in"""
        data = request.json
        user = db.session.execute(db.select(User).filter_by(username=data['username'])).scalar()
        if user and check_password_hash(user.password_hash, data['password']):
            login_user(user)
            return user, 200
        else:
            auth_ns.abort(400, 'Invalid username or password.')

@auth_ns.route('/logout')
class Logout(Resource):
    @login_required
    def post(self):
        """Log the current user out"""
        logout_user()
        return {'message': 'Logged out successfully.'}, 200

@auth_ns.route('/user')
class CurrentUser(Resource):
    @login_required
    @auth_ns.marshal_with(user_model)
    def get(self):
        """Get the current logged-in user's information"""
        return current_user, 200
