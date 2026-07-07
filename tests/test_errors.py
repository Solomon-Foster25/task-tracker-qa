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

def test_get_missing_task_returns_404(client):
    response = client.get("/tasks/9999")
    assert response.status_code == 404

def test_update_missing_task_returns_404(client):
    response = client.patch("/tasks/9999?task_status=done")
    assert response.status_code == 404

def test_delete_missing_task_returns_404(client):
    # regression: TTQ-3 — id that never existed
    response = client.delete("/tasks/9999")
    assert response.status_code == 404

def test_create_task_missing_title_returns_422(client):
    response = client.post("/tasks", json={"body": "no title here", "user_id": 1})
    assert response.status_code == 422

def test_create_task_invalid_status_returns_400(client):
    user = client.post("/users", json={"username": "alice", "email": "alice@example.com"})
    user_id = user.json()["id"]
    response = client.post("/tasks", json={"title": "Test", "body": "x", "user_id": user_id, "status": "banana"})
    assert response.status_code == 400