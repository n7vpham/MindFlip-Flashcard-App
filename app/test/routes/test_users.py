from werkzeug.security import generate_password_hash
import pytest

def test_create_user_route(client):
    response = client.post('/users', data={
        "firstName": "tester",
        "lastName": "lester",
        "email": "testlest@example.com",
        "password": generate_password_hash("testpass")
    })
    assert response.status_code == 308

def test_get_user_by_id_route(client, test_user):
    user_id = test_user['_id']
    response = client.get(f'/users/{user_id}')
    assert response.status_code == 200
    data = response.get_json()
    assert data["email"] == "test@example.com"

@pytest.mark.skip(reason="Not yet implemented")
def test_del_user_by_id_route(client, test_user):
    user_id = test_user['_id']
    response = client.delete(f'/users/{user_id}')
    assert response.status_code == 200

def test_login_user(client, test_user):
    response = client.post('/users/login', data={
        "email": "test@example.com",
        "password": "testpass"
    })
    assert response.status_code == 303

def test_logout_user(client, test_user):
    response = client.get('/users/logout')
    assert response.status_code == 401

    with client.session_transaction() as session:
        session['user_id'] = str(test_user['_id'])

    response = client.get('/users/logout')
    assert response.status_code == 200

def test_get_profile_page(client, test_user):
    response = client.get('/users/profile')
    assert response.status_code == 302

    with client.session_transaction() as session:
        session['user_id'] = str(test_user['_id'])

    response = client.get('/users/profile')
    assert response.status_code == 200

