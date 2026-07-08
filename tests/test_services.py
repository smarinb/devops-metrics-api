def test_create_service_requires_auth(client):
    response = client.post(
        "/services/",
        json={"name": "auth-service", "repository": "github.com/example/auth", "owner": "sergio"},
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


def test_list_services_empty(client):
    response = client.get("/services/")
    assert response.status_code == 200
    assert response.json() == []


def test_get_nonexistent_service(client):
    response = client.get("/services/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Service not found"
