def test_get_notes(client):
    response = client.get('/notes/')
    assert response.status_code == 200