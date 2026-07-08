def test_create_user_and_login(client):
    response = client.post(
        "/users/",
        json={
            "username": "testadmin",
            "email": "testadmin@example.com",
            "role": "admin",
            "password": "testpass123",
        },
    )
    assert response.status_code == 401


def test_full_auth_flow(client, db_session):
    from app.models.user import UserModel
    from app.core.security import hash_password

    user = UserModel(
        username="testadmin",
        email="testadmin@example.com",
        role="admin",
        hashed_password=hash_password("testpass123"),
    )
    db_session.add(user)
    db_session.commit()

    response = client.post(
        "/auth/login",
        data={"username": "testadmin", "password": "testpass123"},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


def test_login_wrong_password(client, db_session):
    from app.models.user import UserModel
    from app.core.security import hash_password

    user = UserModel(
        username="testadmin",
        email="testadmin@example.com",
        role="admin",
        hashed_password=hash_password("testpass123"),
    )
    db_session.add(user)
    db_session.commit()

    response = client.post(
        "/auth/login",
        data={"username": "testadmin", "password": "wrongpassword"},
    )
    assert response.status_code == 401
