def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["database"] == "connected"

def test_starts_empty(client):
    # if the fixture ran, tasks table is empty
    response = client.get("/tasks")
    assert response.status_code == 200
    assert response.json() == []