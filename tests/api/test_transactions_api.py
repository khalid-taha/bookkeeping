# tests/api/test_transactions_api.py

import pytest
from datetime import datetime, timezone
from modules.models.account import Account

@pytest.fixture
def setup_accounts(db):
    debit_account = Account(name='Debit Account', type='Asset')
    credit_account = Account(name='Credit Account', type='Revenue')
    db.session.add_all([debit_account, credit_account])
    db.session.commit()
    return debit_account, credit_account

@pytest.fixture
def new_transaction_data(setup_accounts):
    debit_account, credit_account = setup_accounts
    return {
        'date': datetime.now(timezone.utc).isoformat(),
        'amount': 100.0,
        'description': 'Test Transaction',
        'debit_account_id': debit_account.id,
        'credit_account_id': credit_account.id
    }

def login(client, test_user):
    client.post('/api/auth/login', json={
        'username': test_user.username,
        'password': 'testpass'
    })

def test_get_transactions(client, test_user):
    login(client, test_user)
    response = client.get('/api/transactions/')
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_create_transaction(client, db, test_user, new_transaction_data):
    login(client, test_user)
    response = client.post('/api/transactions/', json=new_transaction_data)
    assert response.status_code == 201
    assert response.json['description'] == new_transaction_data['description']

def test_get_single_transaction(client, db, test_user, new_transaction_data):
    login(client, test_user)
    response = client.post('/api/transactions/', json=new_transaction_data)
    transaction_id = response.json['id']
    response = client.get(f'/api/transactions/{transaction_id}')
    assert response.status_code == 200
    assert response.json['id'] == transaction_id

def test_update_transaction(client, db, test_user, new_transaction_data):
    login(client, test_user)
    response = client.post('/api/transactions/', json=new_transaction_data)
    transaction_id = response.json['id']
    updated_data = {
        'description': 'Updated Transaction',
        'amount': 150.0
    }
    response = client.put(f'/api/transactions/{transaction_id}', json=updated_data)
    assert response.status_code == 200
    assert response.json['description'] == updated_data['description']
    assert response.json['amount'] == updated_data['amount']

def test_delete_transaction(client, db, test_user, new_transaction_data):
    login(client, test_user)
    response = client.post('/api/transactions/', json=new_transaction_data)
    transaction_id = response.json['id']
    response = client.delete(f'/api/transactions/{transaction_id}')
    assert response.status_code == 204
    response = client.get(f'/api/transactions/{transaction_id}')
    assert response.status_code == 404
