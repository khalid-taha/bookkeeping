# tests/api/test_accounts_api.py

import pytest

@pytest.fixture
def new_account_data():
    return {
        'name': 'Test Account',
        'type': 'Asset'
    }

def login(client, test_user):
    client.post('/api/auth/login', json={
        'username': test_user.username,
        'password': 'testpass'
    })

def test_get_accounts(client, test_user):
    login(client, test_user)
    response = client.get('/api/accounts/')
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_create_account(client, db, test_user, new_account_data):
    login(client, test_user)
    response = client.post('/api/accounts/', json=new_account_data)
    assert response.status_code == 201
    assert response.json['name'] == new_account_data['name']

def test_create_duplicate_account(client, db, test_user, new_account_data):
    login(client, test_user)
    client.post('/api/accounts/', json=new_account_data)
    response = client.post('/api/accounts/', json=new_account_data)
    assert response.status_code == 400
    assert 'Account name already exists.' in response.json['message']

def test_get_single_account(client, db, test_user, new_account_data):
    login(client, test_user)
    response = client.post('/api/accounts/', json=new_account_data)
    account_id = response.json['id']
    response = client.get(f'/api/accounts/{account_id}')
    assert response.status_code == 200
    assert response.json['id'] == account_id

def test_update_account(client, db, test_user, new_account_data):
    login(client, test_user)
    response = client.post('/api/accounts/', json=new_account_data)
    account_id = response.json['id']
    updated_data = {'name': 'Updated Account', 'type': 'Liability'}
    response = client.put(f'/api/accounts/{account_id}', json=updated_data)
    assert response.status_code == 200
    assert response.json['name'] == updated_data['name']

def test_delete_account(client, db, test_user, new_account_data):
    login(client, test_user)
    response = client.post('/api/accounts/', json=new_account_data)
    account_id = response.json['id']
    response = client.delete(f'/api/accounts/{account_id}')
    assert response.status_code == 204
    response = client.get(f'/api/accounts/{account_id}')
    assert response.status_code == 404
