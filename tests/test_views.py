# tests/test_views.py

from datetime import date, datetime, timezone
import pytest
from modules.models.account import Account
from modules.models.transaction import Transaction

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
        'submit': 'Create Account'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'Account created successfully.' in response.data

    # Attempt to create the same account again to test uniqueness
    response_duplicate = client.post('/accounts/new', data={
        'name': unique_account_name,
        'type': 'Asset',
        'submit': 'Create Account'
    }, follow_redirects=True)

    assert response_duplicate.status_code == 200
    assert b'Account name already exists.' in response_duplicate.data

def test_new_transaction(client, db, test_user):
    login(client, test_user)
    # Create accounts needed for the transaction
    debit_account = Account(name='Cash_Test', type='Asset')
    credit_account = Account(name='Revenue_Test', type='Revenue')

    db.session.add_all([debit_account, credit_account])
    db.session.commit()

    # Prepare transaction data
    transaction_data = {
        'date': date.today().strftime('%Y-%m-%d'),
        'amount': '500.00',
        'description': 'Test Transaction via Web',
        'debit_account': str(debit_account.id),
        'credit_account': str(credit_account.id),
        'submit': 'Create Transaction'
    }

    # Create the transaction via the web interface
    response = client.post('/transactions/new', data=transaction_data, follow_redirects=True)

    assert response.status_code == 200
    assert b'Transaction created successfully.' in response.data

    # Verify the transaction was saved in the database
    transaction = Transaction.query.filter_by(description='Test Transaction via Web').first()
    assert transaction is not None
    assert transaction.amount == 500.00
    assert transaction.date == date.today()
    assert transaction.debit_account_id == debit_account.id
    assert transaction.credit_account_id == credit_account.id

def test_new_transaction_invalid_data(client, db, test_user):
    login(client, test_user)
    # Prepare incomplete transaction data
    transaction_data = {
        'date': '',
        'amount': '',
        'description': '',
        'debit_account': '',
        'credit_account': '',
        'submit': 'Create Transaction'
    }

    # Attempt to create the transaction
    response = client.post('/transactions/new', data=transaction_data, follow_redirects=True)

    assert response.status_code == 200
    assert b'Please enter a valid date' in response.data
    assert b'Please enter a valid amount' in response.data
    assert b'Description is required' in response.data
    assert b'Please select a debit account' in response.data
    assert b'Please select a credit account' in response.data

    # Ensure no transaction was created
    transaction = Transaction.query.filter_by(description='').first()
    assert transaction is None
