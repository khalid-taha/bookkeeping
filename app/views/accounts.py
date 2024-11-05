# app/views/accounts.py

from flask import Blueprint, render_template, redirect, url_for, flash, request
from modules.forms.account_form import AccountForm
from modules.models.account import Account
from modules.database.db import db
from flask_login import login_required

bp = Blueprint('accounts', __name__, url_prefix='/accounts')

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
    return render_template('account_form.html', form=form)


@bp.route('/', methods=['GET'])
@login_required
def list_accounts():
    accounts = Account.query.all()
    return render_template('account_list.html', accounts=accounts)
