# tests/plugins/test_ml_plugin.py

import json

def test_ml_plugin_post(client):
    # Test POST request with valid input
    response = client.post('/ml/predict', json={'input': [1, 2, 3, 4, 5]})
    assert response.status_code == 200
    data = response.get_json()
    assert data['prediction'] == 15

def test_ml_plugin_post_invalid_input(client):
    # Test POST request with invalid input
    response = client.post('/ml/predict', json={'input': 'invalid'})
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data

def test_ml_plugin_get(client):
    # Test GET request with valid input
    response = client.get('/ml/predict?input=1,2,3,4,5')
    assert response.status_code == 200
    data = response.get_json()
    assert data['prediction'] == 15.0

def test_ml_plugin_get_no_input(client):
    # Test GET request without input
    response = client.get('/ml/predict')
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data

def test_ml_plugin_get_invalid_input(client):
    # Test GET request with invalid input
    response = client.get('/ml/predict?input=a,b,c')
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data
