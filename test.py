import pytest
import json
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# Extension 1
def test_user_create_and_delete_post(client):
    # Create a user
    response_user = client.post('/user')
    assert response_user.status_code == 200
    user_data = json.loads(response_user.data.decode('utf-8'))
    user_id = user_data['id']
    user_key = user_data['key']

    # Create a post
    response_create_post = client.post('/post', json={'msg': 'Test message', 'user_id': user_id, 'user_key': user_key})
    assert response_create_post.status_code == 200
    post_data = json.loads(response_create_post.data.decode('utf-8'))
    post_id = post_data['id']

    response_read_post = client.get(f'/post/{post_id}')
    assert response_read_post.status_code == 200

    response_delete_post = client.delete(f'/post/{post_id}/delete/{user_key}')
    assert response_delete_post.status_code == 200

    response_deleted_post = client.get(f'/post/{post_id}')
    assert response_deleted_post.status_code == 404

# Extension 4
def test_search_posts_by_timestamp(client):
    response = client.get('/posts/search?start_timestamp=2023-01-01T00:00:00&end_timestamp=2023-12-31T23:59:59')
    assert response.status_code == 200
    data = json.loads(response.data.decode('utf-8'))
    assert isinstance(data, list)

# Extension 1
def test_create_user(client):
    response = client.post('/user')
    assert response.status_code == 200
    data = json.loads(response.data.decode('utf-8'))
    assert 'id' in data
    assert 'key' in data

# Extension 5
def test_search_posts_by_user(client):
    response = client.get('/posts/user/1')
    assert response.status_code == 200
    data = json.loads(response.data.decode('utf-8'))
    assert isinstance(data, list)

# Extension 3 and 6
def test_get_thread_for_post(client):
    response = client.get('/posts/thread/2')
    assert response.status_code == 200
    data = json.loads(response.data.decode('utf-8'))
    assert isinstance(data, list)
