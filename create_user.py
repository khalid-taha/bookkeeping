# create_user.py

from app import create_app
from modules.database.db import db
from modules.models.user import User
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    # Replace 'admin' and 'admin123' with your desired username and password
    username = 'admin'
    password = 'securepassword123'
    role = 'Admin'

    # Check if the user already exists
    if not User.query.filter_by(username=username).first():
        user = User(
            username=username,
            password_hash=generate_password_hash(password),
            role=role
        )
        db.session.add(user)
        db.session.commit()
        print(f'User {username} created successfully.')
    else:
        print(f'User {username} already exists.')
