# app/api/accounts_api.py

from flask import request
from flask_restx import Namespace, Resource, fields
from modules.models.account import Account
from modules.database.db import db
from flask_login import login_required
from . import api

accounts_ns = Namespace('accounts', description='Accounts related operations')

account_model = accounts_ns.model('Account', {
    'id': fields.Integer(readOnly=True, description='The unique identifier of an account'),
    'name': fields.String(required=True, description='Account name'),
    'type': fields.String(required=True, description='Account type')
})

@accounts_ns.route('/')
class AccountList(Resource):
    @accounts_ns.marshal_list_with(account_model)
    @login_required
    def get(self):
        """List all accounts"""
        accounts = Account.query.all()
        return accounts, 200

    @accounts_ns.expect(account_model, validate=True)
    @accounts_ns.marshal_with(account_model, code=201)
    @login_required
    def post(self):
        """Create a new account"""
        data = request.json
        if db.session.execute(db.select(Account).filter_by(name=data['name'])).scalar():
            accounts_ns.abort(400, 'Account name already exists.')
        new_account = Account(name=data['name'], type=data['type'])
        db.session.add(new_account)
        db.session.commit()
        return new_account, 201

@accounts_ns.route('/<int:id>')
@accounts_ns.response(404, 'Account not found')
@accounts_ns.param('id', 'The account identifier')
class AccountResource(Resource):
    @accounts_ns.marshal_with(account_model)
    @login_required
    def get(self, id):
        """Fetch a given account"""
        account = db.session.get(Account, id)
        if not account:
            accounts_ns.abort(404, 'Account not found')
        return account, 200

    @accounts_ns.expect(account_model, validate=True)
    @accounts_ns.marshal_with(account_model)
    @login_required
    def put(self, id):
        """Update a given account"""
        account = db.session.get(Account, id)
        if not account:
            accounts_ns.abort(404, 'Account not found')
        data = request.json
        if 'name' in data:
            if db.session.execute(db.select(Account).filter(Account.name == data['name'], Account.id != id)).scalar():
                accounts_ns.abort(400, 'Another account with this name already exists.')
            account.name = data['name']
        if 'type' in data:
            account.type = data['type']
        db.session.commit()
        return account, 200

    @accounts_ns.response(204, 'Account deleted')
    @login_required
    def delete(self, id):
        """Delete a given account"""
        account = db.session.get(Account, id)
        if not account:
            accounts_ns.abort(404, 'Account not found')
        db.session.delete(account)
        db.session.commit()
        return '', 204
