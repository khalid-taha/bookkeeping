# modules/services/schemas.py

from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from modules.models.account import Account
from modules.models.transaction import Transaction
from modules.models.user import User

class AccountSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Account
        load_instance = True

class TransactionSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Transaction
        load_instance = True

class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        exclude = ('password_hash',)
