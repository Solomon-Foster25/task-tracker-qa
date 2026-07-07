def test_create_user(client):
    response = client.post("/users", json={
        "username": "alice",
        "email": "alice@example.com",
    })
    assert response.status_code == 201          # correct "created" code
    data = response.json()
    assert data["username"] == "alice"          # echoes back what we sent
    assert data["email"] == "alice@example.com"
    assert "id" in data                          # DB assigned an id
    assert data["id"] == 1                        # first user, thanks to RESTART IDENTITY