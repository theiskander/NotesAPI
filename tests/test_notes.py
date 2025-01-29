def test_get_notes(client):
    response = client.get('/notes/')
    assert response.status_code == 200

def test_create_note(client):
    payload = {'title': 'Test Note', 'content': 'This is a test note'}
    response = client.post('/notes/create', json=payload)
    assert response.status_code == 201