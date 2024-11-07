# tests/test_views.py

from datetime import date, datetime, timezone
import pytest
from modules.models.account import Account
from modules.models.transaction import Transaction
from modules.database.db import db  # Import db to access db.session.get()

def login(client, test_user):
    # Log in the test client
    response = client.post('/auth/login', data={
        'username': test_user.username,
        'password': 'testpass'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Logged in successfully.' in response.data

def test_new_account(client, db, test_user):
    login(client, test_user)
    # Create a unique account name using timestamp
    unique_account_name = f'Bank_Test_{datetime.now(timezone.utc).timestamp()}'

    # Create the account successfully
    response = client.post('/accounts/new', data={
        'name': unique_account_name,
        'type': 'Asset',
        'submit': 'Submit'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'Account created successfully.' in response.data

def test_edit_account(client, db, test_user):
    login(client, test_user)
    # Create an account to edit
    account = Account(name='Edit_Test_Account', type='Asset')
    db.session.add(account)
    db.session.commit()

    # Edit the account
    response = client.post(f'/accounts/{account.id}/edit', data={
        'name': 'Edited Account',
        'type': 'Liability',
        'submit': 'Submit'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'Account updated successfully.' in response.data
    # Updated to use db.session.get()
    updated_account = db.session.get(Account, account.id)
    assert updated_account.name == 'Edited Account'
    assert updated_account.type == 'Liability'

def test_delete_account(client, db, test_user):
    login(client, test_user)
    # Create an account to delete
    account = Account(name='Delete_Test_Account', type='Asset')
    db.session.add(account)
    db.session.commit()

    # Delete the account
    response = client.post(f'/accounts/{account.id}/delete', follow_redirects=True)

    assert response.status_code == 200
    assert b'Account deleted successfully.' in response.data
    # Updated to use db.session.get()
    deleted_account = db.session.get(Account, account.id)
    assert deleted_account is None

def test_edit_nonexistent_account(client, test_user):
    login(client, test_user)
    response = client.get('/accounts/99999/edit')
    assert response.status_code == 404

def test_delete_nonexistent_account(client, test_user):
    login(client, test_user)
    response = client.post('/accounts/99999/delete', follow_redirects=True)
    assert response.status_code == 404
