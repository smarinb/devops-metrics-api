from app.models.user import UserModel
from app.core.security import hash_password


def get_auth_token(client, db_session):
    user = UserModel(
        username="admin_metrics",
        email="admin_metrics@example.com",
        role="admin",
        hashed_password=hash_password("adminpass123"),
    )
    db_session.add(user)
    db_session.commit()

    response = client.post(
        "/auth/login",
        data={"username": "admin_metrics", "password": "adminpass123"},
    )
    return response.json()["access_token"]


def test_metrics_summary_empty(client):
    response = client.get("/metrics/summary")
    assert response.status_code == 200
    data = response.json()
    assert data["total_deployments"] == 0
    assert data["overall_success_rate"] == 0.0
    assert data["by_service"] == []


def test_metrics_summary_with_data(client, db_session):
    token = get_auth_token(client, db_session)

    service_response = client.post(
        "/services/",
        json={"name": "metrics-service", "repository": "github.com/test/metrics", "owner": "sergio"},
        headers={"Authorization": f"Bearer {token}"},
    )
    service_id = service_response.json()["id"]

    client.post(
        "/deployments/",
        json={"service_id": service_id, "version": "v1", "environment": "production", "status": "success", "duration_seconds": 10},
        headers={"Authorization": f"Bearer {token}"},
    )
    client.post(
        "/deployments/",
        json={"service_id": service_id, "version": "v2", "environment": "production", "status": "failed", "duration_seconds": 20},
        headers={"Authorization": f"Bearer {token}"},
    )

    response = client.get("/metrics/summary")
    assert response.status_code == 200
    data = response.json()
    assert data["total_deployments"] == 2
    assert data["overall_success_rate"] == 50.0
    assert len(data["by_service"]) == 1
    assert data["by_service"][0]["success_rate"] == 50.0
    assert data["by_service"][0]["avg_duration_seconds"] == 15.0
