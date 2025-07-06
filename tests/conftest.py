
import pytest
from fastapi.testclient import TestClient
from tickethub.main import app
import os
from dotenv import load_dotenv

@pytest.fixture
def client():
   return TestClient(app)

@pytest.fixture
def auth_headers(client):
    # perform a real login to get a token
    resp = client.post(
        "/auth/login",
        json={"username": "emilys", "password": "emilyspass"}
    )
    assert resp.status_code == 200, "Login failed in fixture"
    token = resp.json()["token"]
    return {"Authorization": f"Bearer {token}"}

os.environ["APP_ENV"] = "test"

load_dotenv(".env.test", override=True)
