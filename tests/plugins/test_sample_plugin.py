# tests/plugins/test_sample_plugin.py

def test_sample_plugin(client):
    response = client.get('/sample_plugin/')
    assert response.status_code == 200
    assert response.data.decode() == 'Hello from Sample Plugin!'

