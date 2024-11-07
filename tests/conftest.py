# tests/conftest.py

import pytest
from app import create_app
from modules.database.db import db as _db
from modules.models.user import User
from werkzeug.security import generate_password_hash

@pytest.fixture(scope='function')
def app():
    app = create_app('config.TestingConfig')  # Use TestingConfig
    app.config['TESTING'] = True

    with app.app_context():
        yield app

@pytest.fixture(scope='function')
def db(app):
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
        yield _db
        _db.session.close()
        _db.drop_all()

@pytest.fixture(scope='function')
def client(app, db):
    with app.test_client() as client:
        # Log in the test user
        client.post('/auth/login', data={
            'username': 'testuser',
            'password': 'testpassword'
        }, follow_redirects=True)
        yield client
        # No need to logout and rollback, as the database is dropped after each test
