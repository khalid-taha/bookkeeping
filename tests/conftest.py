# tests/conftest.py

import pytest
from app import create_app
from modules.database.db import db as _db
from modules.models.user import User
from werkzeug.security import generate_password_hash

@pytest.fixture(scope='function')
def app():
    app = create_app('config.TestingConfig')
    app.config['TESTING'] = True
    with app.app_context():
        yield app

@pytest.fixture(scope='function')
def db(app):
    _db.create_all()
    yield _db
    _db.session.remove()
    _db.drop_all()

@pytest.fixture(scope='function')
def test_user(db):
    user = User(
        username='testuser',
        password_hash=generate_password_hash('testpass'),
        role='User'
    )
    db.session.add(user)
    db.session.commit()
    return user

@pytest.fixture(scope='function')
def client(app, db):
    return app.test_client()
