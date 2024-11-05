# app/views/transactions.py

from flask import Blueprint, render_template, redirect, url_for, flash, request
from modules.forms.transaction_form import TransactionForm
from modules.models.transaction import Transaction
from modules.models.account import Account
from modules.database.db import db
from sqlalchemy.exc import IntegrityError
from flask_login import login_required

bp = Blueprint('transactions', __name__, url_prefix='/transactions')

@bp.route('/new', methods=['GET', 'POST'])
@login_required
def new_transaction():
    form = TransactionForm()
    # Populate account choices
    form.debit_account.choices = [(account.id, account.name) for account in Account.query.all()]
    form.credit_account.choices = [(account.id, account.name) for account in Account.query.all()]
    
    if form.validate_on_submit():
        transaction = Transaction(
            date=form.date.data,
            amount=form.amount.data,
            description=form.description.data,
            debit_account_id=form.debit_account.data,
            credit_account_id=form.credit_account.data
        )
        db.session.add(transaction)
        try:
            db.session.commit()
            flash('Transaction created successfully.', 'success')
            return redirect(url_for('transactions.list_transactions'))
        except IntegrityError:
            db.session.rollback()
            flash('Error creating transaction.', 'danger')
            return render_template('transaction_form.html', form=form), 400
    return render_template('transaction_form.html', form=form)

@bp.route('/', methods=['GET'])
@login_required
def list_transactions():
    transactions = Transaction.query.all()
    return render_template('transaction_list.html', transactions=transactions)
