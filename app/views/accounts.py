# app/views/accounts.py

from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from modules.forms.account_form import AccountForm
from modules.models.account import Account
from modules.database.db import db
from flask_login import login_required

bp = Blueprint('accounts', __name__, url_prefix='/accounts')

@bp.route('/', methods=['GET'])
@login_required
def list_accounts():
    accounts = Account.query.all()
    return render_template('account_list.html', accounts=accounts)

@bp.route('/new', methods=['GET', 'POST'])
@login_required
def new_account():
    form = AccountForm()
    if form.validate_on_submit():
        account = Account(
            name=form.name.data,
            type=form.type.data
        )
        db.session.add(account)
        db.session.commit()
        flash('Account created successfully.', 'success')
        return redirect(url_for('accounts.list_accounts'))
    return render_template('account_form.html', form=form, title='Create Account')

@bp.route('/<int:account_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_account(account_id):
    # Updated to use db.session.get() and handle 404 manually
    account = db.session.get(Account, account_id)
    if not account:
        abort(404)
    form = AccountForm(obj=account)
    if form.validate_on_submit():
        if Account.query.filter(Account.name == form.name.data, Account.id != account.id).first():
            form.name.errors.append('Account name already exists.')
        else:
            account.name = form.name.data
            account.type = form.type.data
            db.session.commit()
            flash('Account updated successfully.', 'success')
            return redirect(url_for('accounts.list_accounts'))
    return render_template('account_form.html', form=form, title='Edit Account')

@bp.route('/<int:account_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_account(account_id):
    # Updated to use db.session.get() and handle 404 manually
    account = db.session.get(Account, account_id)
    if not account:
        abort(404)
    if request.method == 'POST':
        db.session.delete(account)
        db.session.commit()
        flash('Account deleted successfully.', 'success')
        return redirect(url_for('accounts.list_accounts'))
    return render_template('account_confirm_delete.html', account=account)
