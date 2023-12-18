import pytest
import json
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_search_posts_by_timestamp(client):
    response = client.get('/posts/search?start_timestamp=2023-01-01T00:00:00&end_timestamp=2023-12-31T23:59:59')
    assert response.status_code == 200
    data = json.loads(response.data.decode('utf-8'))
    assert isinstance(data, list)

def test_create_user(client):
    response = client.post('/user')
    assert response.status_code == 200
    data = json.loads(response.data.decode('utf-8'))
    assert 'id' in data
    assert 'key' in data

def test_search_posts_by_user(client):
    response = client.get('/posts/user/1')
    assert response.status_code == 200
    data = json.loads(response.data.decode('utf-8'))
    assert isinstance(data, list)

def test_get_thread_for_post(client):
    response = client.get('/posts/thread/2')
    assert response.status_code == 200
    data = json.loads(response.data.decode('utf-8'))
    assert isinstance(data, list)

