
def test_login_success(client):
    """POST /login with valid credentials should return token info."""
    response = client.post("/auth/login", json={
        "username": "emilys",
        "password": "emilyspass"
    })
    assert response.status_code == 200

    data = response.json()
    assert "token" in data
    assert "username" in data
    assert "email" in data
    assert data["username"] == "emilys"


def test_login_invalid_credentials(client):
    """POST /login with bad credentials should return 401."""
    response = client.post("/auth/login", json={
        "username": "wronguser",
        "password": "wrongpass"
    })
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"


def test_login_missing_fields(client):
    """POST /login with missing fields should return 422."""
    response = client.post("/auth/login", json={"username": "useronly"})
    assert response.status_code == 422

