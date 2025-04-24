from werkzeug.security import generate_password_hash

def test_create_user_route(client, test_user):
    response = client.post('/users', data={
        "firstName": "tester",
        "lastName": "lester",
        "email": "testlest@example.com",
        "password": generate_password_hash("testpass")
    })
    assert response.status_code == 308
