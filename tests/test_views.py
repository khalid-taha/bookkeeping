# tests/test_views.py

from datetime import date, datetime, timezone
import pytest
from modules.models.account import Account
from modules.models.transaction import Transaction

def test_new_account(client, db):
    # Create a unique account name using timestamp
    unique_account_name = f'Bank_Test_{datetime.now(timezone.utc).timestamp()}'

    # Create the account successfully
    response = client.post('/accounts/new', data={
        'name': unique_account_name,
        'type': 'Asset'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'Account created successfully.' in response.data  # Adjust based on your flash message

    # Attempt to create the same account again to test uniqueness
    response_duplicate = client.post('/accounts/new', data={
        'name': unique_account_name,
        'type': 'Asset'
    }, follow_redirects=True)

    assert response_duplicate.status_code == 200  # Expecting OK status with form re-rendered
    assert b'Account name already exists.' in response_duplicate.data  # Verify error message

def test_new_transaction(client, db):
    # Create accounts needed for the transaction
    debit_account = Account(name='Cash_Test', type='Asset')
    credit_account = Account(name='Revenue_Test', type='Revenue')

    db.session.add_all([debit_account, credit_account])
    db.session.commit()

    # Prepare transaction data
    transaction_data = {
        'date': date.today().strftime('%Y-%m-%d'),  # Format date as string
        'amount': '500.00',  # Amount must be a string when simulating form data
        'description': 'Test Transaction via Web',
        'debit_account': str(debit_account.id),
        'credit_account': str(credit_account.id),
        'submit': 'Create Transaction'
    }

    # Create the transaction via the web interface
    response = client.post('/transactions/new', data=transaction_data, follow_redirects=True)

    # Assert the response indicates success
    assert response.status_code == 200  # Adjust if you expect a redirect (e.g., 302)
    assert b'Transaction created successfully.' in response.data  # Check for success message

    # Verify the transaction was saved in the database
    transaction = Transaction.query.filter_by(description='Test Transaction via Web').first()
    assert transaction is not None
    assert transaction.amount == 500.00
    assert transaction.date == date.today()
    assert transaction.debit_account_id == debit_account.id
    assert transaction.credit_account_id == credit_account.id

def test_new_transaction_invalid_data(client, db):
    # Prepare incomplete transaction data
    transaction_data = {
        'date': '',  # Missing date
        'amount': '',  # Missing amount
        'description': '',  # Missing description
        'debit_account': '',  # Missing debit account
        'credit_account': '',  # Missing credit account
        'submit': 'Create Transaction'
    }

    # Attempt to create the transaction
    response = client.post('/transactions/new', data=transaction_data, follow_redirects=True)

    # Assert the form re-renders with errors
    assert response.status_code == 200
    assert b'Please enter a valid date' in response.data
    assert b'Please enter a valid amount' in response.data
    assert b'Description is required' in response.data
    assert b'Please select a debit account' in response.data
    assert b'Please select a credit account' in response.data

    # Ensure no transaction was created
    transaction = Transaction.query.filter_by(description='').first()
    assert transaction is None
