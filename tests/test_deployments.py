from app.models.user import UserModel
from app.core.security import hash_password


def get_auth_token(client, db_session):
    user = UserModel(
        username="admin_test",
        email="admin_test@example.com",
        role="admin",
        hashed_password=hash_password("adminpass123"),
    )
    db_session.add(user)
    db_session.commit()

    response = client.post(
        "/auth/login",
        data={"username": "admin_test", "password": "adminpass123"},
    )
    return response.json()["access_token"]


def create_service(client, token):
    response = client.post(
        "/services/",
        json={"name": "test-service", "repository": "github.com/test/test", "owner": "sergio"},
        headers={"Authorization": f"Bearer {token}"},
    )
    return response.json()["id"]


def test_create_deployment(client, db_session):
    token = get_auth_token(client, db_session)
    service_id = create_service(client, token)

    response = client.post(
        "/deployments/",
        json={
            "service_id": service_id,
            "version": "v1.0.0",
            "environment": "production",
            "status": "success",
            "duration_seconds": 30.5,
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["version"] == "v1.0.0"
    assert data["status"] == "success"


def test_create_deployment_invalid_status(client, db_session):
    token = get_auth_token(client, db_session)
    service_id = create_service(client, token)

    response = client.post(
        "/deployments/",
        json={
            "service_id": service_id,
            "version": "v1.0.0",
            "environment": "production",
            "status": "invalid_status",
            "duration_seconds": 30.5,
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 422


def test_filter_deployments_by_environment(client, db_session):
    token = get_auth_token(client, db_session)
    service_id = create_service(client, token)

    client.post(
        "/deployments/",
        json={"service_id": service_id, "version": "v1", "environment": "staging", "status": "success", "duration_seconds": 10},
        headers={"Authorization": f"Bearer {token}"},
    )
    client.post(
        "/deployments/",
        json={"service_id": service_id, "version": "v2", "environment": "production", "status": "success", "duration_seconds": 15},
        headers={"Authorization": f"Bearer {token}"},
    )

    response = client.get("/deployments/?environment=production")
    assert response.status_code == 200
    results = response.json()
    assert len(results) == 1
    assert results[0]["environment"] == "production"
