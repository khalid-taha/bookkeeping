# modules/models/account.py

from modules.database.db import db

class Account(db.Model):
    __tablename__ = 'accounts'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=False)
    type = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"<Account {self.name}>"
