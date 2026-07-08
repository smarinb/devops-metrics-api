from app.models.user import UserModel
from app.core.security import hash_password


def get_auth_token(client, db_session):
    user = UserModel(
        username="admin_users",
        email="admin_users@example.com",
        role="admin",
        hashed_password=hash_password("adminpass123"),
    )
    db_session.add(user)
    db_session.commit()

    response = client.post(
        "/auth/login",
        data={"username": "admin_users", "password": "adminpass123"},
    )
    return response.json()["access_token"]


def test_create_user_password_not_in_response(client, db_session):
    token = get_auth_token(client, db_session)

    response = client.post(
        "/users/",
        json={
            "username": "newuser",
            "email": "newuser@example.com",
            "role": "viewer",
            "password": "secretpass123",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 201
    data = response.json()
    assert "password" not in data
    assert "hashed_password" not in data


def test_list_users(client, db_session):
    token = get_auth_token(client, db_session)

    client.post(
        "/users/",
        json={"username": "user1", "email": "user1@example.com", "role": "viewer", "password": "pass123456"},
        headers={"Authorization": f"Bearer {token}"},
    )

    response = client.get("/users/")
    assert response.status_code == 200
    usernames = [u["username"] for u in response.json()]
    assert "admin_users" in usernames
    assert "user1" in usernames


def test_get_nonexistent_user(client):
    response = client.get("/users/999")
    assert response.status_code == 404
