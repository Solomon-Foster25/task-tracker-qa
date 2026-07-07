def test_create_task(client):
    user = client.post("/users", json={"username": "alice", "email": "alice@example.com",})
    user_id = user.json()["id"]

    response = client.post("/tasks", json = {"title": "New task", "body": "task body", "user_id": user_id, "status":"todo",})
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 1
    assert data["title"] == "New task"
    assert data["body"] == "task body"
    assert data["user_id"] == user_id
    assert data["status"] == "todo"
     
def test_get_task(client): 
    user = client.post("/users", json={"username": "alice", "email": "alice@example.com",})
    user_id = user.json()["id"]
    create_task = client.post("/tasks", json = {"title": "New task", "body": "task body", "user_id": user_id, "status":"todo",})
    task_id = create_task.json()["id"]
    
    response = client.get(f"/tasks/{task_id}")
    data = response.json()

    assert response.status_code == 200
    assert data["id"] == task_id
    assert data["title"] == "New task"
    assert data["user_id"] == user_id

def test_list_task(client):
    user = client.post("/users", json={"username": "alice", "email": "alice@example.com",})
    user_id = user.json()["id"]
    create_task = client.post("/tasks", json = {"title": "New task", "body": "task body", "user_id": user_id, "status":"todo",})
    create_task2 = client.post("/tasks", json = {"title": "New task2", "body": "task body", "user_id": user_id, "status":"todo",})

    response = client.get("/tasks")
    data = response.json()

    assert response.status_code == 200
    assert len(data) == 2
    titles = [task["title"] for task in data]
    assert "New task" in titles
    assert "New task2" in titles

def test_update_task(client):
    user = client.post("/users", json={"username": "alice", "email": "alice@example.com",})
    user_id = user.json()["id"]
    create_task = client.post("/tasks", json = {"title": "New task", "body": "task body", "user_id": user_id, "status":"todo",})
    task_id = create_task.json()["id"]

    update_task = client.patch(f"/tasks/{task_id}?task_status=in_progress")

    assert update_task.status_code == 200
    assert update_task.json()["status"] == "in_progress"

    response = client.get(f"/tasks/{task_id}")
    data = response.json()
    assert data["status"] == "in_progress"

def test_delete_task(client):
    user = client.post("/users", json={"username": "alice", "email": "alice@example.com",})
    user_id = user.json()["id"]
    create_task = client.post("/tasks", json = {"title": "New task", "body": "task body", "user_id": user_id, "status":"todo",})
    task_id = create_task.json()["id"]

    delete_task = client.delete(f"/tasks/{task_id}")

    assert delete_task.status_code == 204

    response = client.get(f"/tasks/{task_id}")

    assert response.status_code == 404