
import pytest
from fastapi.testclient import TestClient
from tickethub.main import app

@pytest.fixture
def client():
    """TestClient fixture for FastAPI app."""
    return TestClient(app)


