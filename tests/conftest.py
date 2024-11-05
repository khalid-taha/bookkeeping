# tests/conftest.py

import pytest
from app import create_app
from modules.database.db import db as _db
from modules.models.user import User
from werkzeug.security import generate_password_hash

@pytest.fixture(scope='session')
def app():
    app = create_app('config.TestingConfig')  # Use TestingConfig
    app.config['TESTING'] = True
    # The following configurations are already set in TestingConfig
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    # app.config['WTF_CSRF_ENABLED'] = False

    with app.app_context():
        _db.create_all()
        # Create a test user
        test_user = User(
            username='testuser',
            password_hash=generate_password_hash('testpassword'),
            role='Admin'
        )
        _db.session.add(test_user)
        _db.session.commit()
        yield app
        _db.drop_all()

@pytest.fixture(scope='session')
def db(app):
    return _db

@pytest.fixture(scope='function')
def client(app, db):
    with app.test_client() as client:
        # Log in the test user
        response = client.post('/auth/login', data={
            'username': 'testuser',
            'password': 'testpassword'
        }, follow_redirects=True)
        yield client
        # Log out after test
        response = client.get('/auth/logout', follow_redirects=True)
        # Rollback the session to clean up after the test
        db.session.rollback()
