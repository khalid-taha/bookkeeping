# app/api/transactions_api.py

from flask import request
from flask_restx import Namespace, Resource, fields
from modules.models.transaction import Transaction
from modules.models.account import Account
from modules.database.db import db
from flask_login import login_required
from . import api
from dateutil import parser

transactions_ns = Namespace('transactions', description='Transactions related operations')

transaction_model = transactions_ns.model('Transaction', {
    'id': fields.Integer(readOnly=True, description='The unique identifier of a transaction'),
    'date': fields.DateTime(required=True, description='Date of the transaction'),
    'amount': fields.Float(required=True, description='Amount of the transaction'),
    'description': fields.String(required=True, description='Description of the transaction'),
    'debit_account_id': fields.Integer(required=True, description='Debit account ID'),
    'credit_account_id': fields.Integer(required=True, description='Credit account ID')
})

transaction_update_model = transactions_ns.model('TransactionUpdate', {
    'date': fields.DateTime(description='Date of the transaction'),
    'amount': fields.Float(description='Amount of the transaction'),
    'description': fields.String(description='Description of the transaction'),
    'debit_account_id': fields.Integer(description='Debit account ID'),
    'credit_account_id': fields.Integer(description='Credit account ID')
})

@transactions_ns.route('/')
class TransactionList(Resource):
    @transactions_ns.marshal_list_with(transaction_model)
    @login_required
    def get(self):
        """List all transactions"""
        transactions = Transaction.query.all()
        return transactions, 200

    @transactions_ns.expect(transaction_model, validate=True)
    @transactions_ns.marshal_with(transaction_model, code=201)
    @login_required
    def post(self):
        """Create a new transaction"""
        data = request.json
        required_fields = ['date', 'amount', 'description', 'debit_account_id', 'credit_account_id']
        if not all(field in data for field in required_fields):
            transactions_ns.abort(400, 'All fields are required.')

        # Validate accounts exist
        debit_account = db.session.get(Account, data['debit_account_id'])
        credit_account = db.session.get(Account, data['credit_account_id'])
        if not debit_account or not credit_account:
            transactions_ns.abort(400, 'Invalid debit or credit account ID.')

        # Parse and validate date
        try:
            date = parser.isoparse(data['date'])
        except (ValueError, TypeError):
            transactions_ns.abort(400, 'Invalid date format.')

        new_transaction = Transaction(
            date=date,
            amount=data['amount'],
            description=data['description'],
            debit_account_id=data['debit_account_id'],
            credit_account_id=data['credit_account_id']
        )
        db.session.add(new_transaction)
        db.session.commit()
        return new_transaction, 201

@transactions_ns.route('/<int:id>')
@transactions_ns.response(404, 'Transaction not found')
@transactions_ns.param('id', 'The transaction identifier')
class TransactionResource(Resource):
    @transactions_ns.marshal_with(transaction_model)
    @login_required
    def get(self, id):
        """Fetch a given transaction"""
        transaction = db.session.get(Transaction, id)
        if not transaction:
            transactions_ns.abort(404, 'Transaction not found')
        return transaction, 200

    @transactions_ns.expect(transaction_update_model, validate=True)
    @transactions_ns.marshal_with(transaction_model)
    @login_required
    def put(self, id):
        """Update a given transaction"""
        transaction = db.session.get(Transaction, id)
        if not transaction:
            transactions_ns.abort(404, 'Transaction not found')
        data = request.json

        if 'date' in data:
            try:
                transaction.date = parser.isoparse(data['date'])
            except (ValueError, TypeError):
                transactions_ns.abort(400, 'Invalid date format.')

        if 'amount' in data:
            transaction.amount = data['amount']

        if 'description' in data:
            transaction.description = data['description']

        if 'debit_account_id' in data:
            debit_account = db.session.get(Account, data['debit_account_id'])
            if not debit_account:
                transactions_ns.abort(400, 'Invalid debit account ID.')
            transaction.debit_account_id = data['debit_account_id']

        if 'credit_account_id' in data:
            credit_account = db.session.get(Account, data['credit_account_id'])
            if not credit_account:
                transactions_ns.abort(400, 'Invalid credit account ID.')
            transaction.credit_account_id = data['credit_account_id']

        db.session.commit()
        return transaction, 200

    @transactions_ns.response(204, 'Transaction deleted')
    @login_required
    def delete(self, id):
        """Delete a given transaction"""
        transaction = db.session.get(Transaction, id)
        if not transaction:
            transactions_ns.abort(404, 'Transaction not found')
        db.session.delete(transaction)
        db.session.commit()
        return '', 204
