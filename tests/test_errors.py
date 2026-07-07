def test_duplicate_user_returns_409(client):
    payload = {"username": "alice", "email": "alice@example.com"}
    client.post("/users", json=payload)                # first create succeeds
    response = client.post("/users", json=payload)     # exact duplicate
    assert response.status_code == 409                 # currently 500 → TTQ-1

def test_non_existent_user_returns_404(client):
    payload = {"title": "Test title", "body": "task body", "user_id": 9999}
    client.post("/tasks", json=payload)
    response = client.post("/tasks", json=payload)
    assert response.status_code == 404