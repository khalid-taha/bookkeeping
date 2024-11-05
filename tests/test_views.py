# tests/test_views.py

from datetime import datetime, timezone
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
    assert b'Account created successfully' in response.data  # Adjust based on your flash message

    # Attempt to create the same account again to test uniqueness
    response_duplicate = client.post('/accounts/new', data={
        'name': unique_account_name,
        'type': 'Asset'
    }, follow_redirects=True)

    assert response_duplicate.status_code == 200  # Expecting OK status with form re-rendered
    assert b'Account name already exists' in response_duplicate.data  # Verify error message
