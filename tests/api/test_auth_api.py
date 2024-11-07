# tests/api/test_auth_api.py

import pytest

def test_login(client, test_user):
    response = client.post('/api/auth/login', json={
        'username': test_user.username,
        'password': 'testpass'
    })
    assert response.status_code == 200
    assert response.json['username'] == test_user.username

def test_login_invalid_credentials(client):
    response = client.post('/api/auth/login', json={
        'username': 'wronguser',
        'password': 'wrongpass'
    })
    assert response.status_code == 400
    assert 'Invalid username or password.' in response.json['message']

def test_get_current_user(client, test_user):
    # Log in first
    client.post('/api/auth/login', json={
        'username': test_user.username,
        'password': 'testpass'
    })

    # Get current user
    response = client.get('/api/auth/user')
    assert response.status_code == 200
    assert response.json['username'] == test_user.username

def test_logout(client, test_user):
    # Log in first
    client.post('/api/auth/login', json={
        'username': test_user.username,
        'password': 'testpass'
    })

    # Log out
    response = client.post('/api/auth/logout')
    assert response.status_code == 200
    assert response.json['message'] == 'Logged out successfully.'

    # Attempt to access protected endpoint
    response = client.get('/api/auth/user')
    assert response.status_code == 401 or response.status_code == 302  # Depending on your setup
