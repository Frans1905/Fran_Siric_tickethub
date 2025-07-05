import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from fastapi import HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials

from tickethub.services.auth_service import get_token, verify_token

@pytest.mark.asyncio
@patch("tickethub.services.auth_service.httpx.AsyncClient")
async def test_get_token_success(mock_client_class):
    mock_client = AsyncMock()
    mock_resp = AsyncMock()
    mock_resp.status_code = 200
    mock_resp.json = MagicMock(return_value={
        "accessToken": "abc123",
        "username": "user1",
        "email": "user1@example.com"
    })
    mock_client.post.return_value = mock_resp
    mock_client_class.return_value.__aenter__.return_value = mock_client

    token = await get_token("emilys", "emilyspass")
    assert token["token"] == "abc123"

@pytest.mark.asyncio
@patch("tickethub.services.auth_service.httpx.AsyncClient")
async def test_get_token_failure(mock_client_class):
    mock_client = AsyncMock()
    mock_resp = AsyncMock()
    mock_resp.status_code = 401
    mock_resp.json.return_value = {}
    mock_client.post.return_value = mock_resp
    mock_client_class.return_value.__aenter__.return_value = mock_client

    with pytest.raises(HTTPException) as exc:
        await get_token("baduser", "badpass")
    assert exc.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert exc.value.detail == "Invalid credentials"

@pytest.mark.asyncio
@patch("tickethub.services.auth_service.httpx.AsyncClient")
async def test_verify_token_success(mock_client_class):
    creds = HTTPAuthorizationCredentials(scheme="Bearer", credentials="validtoken")
    mock_client = AsyncMock()
    mock_resp = AsyncMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {"id": 1, "username": "user1"}
    mock_client.get.return_value = mock_resp
    mock_client_class.return_value.__aenter__.return_value = mock_client

    token_out = await verify_token(creds)
    assert token_out == "validtoken"

@pytest.mark.asyncio
@patch("tickethub.services.auth_service.httpx.AsyncClient")
async def test_verify_token_failure(mock_client_class):
    creds = HTTPAuthorizationCredentials(scheme="Bearer", credentials="invalidtoken")
    mock_client = AsyncMock()
    mock_resp = AsyncMock()
    mock_resp.status_code = 401
    mock_resp.json.return_value = {"message": "Unauthorized"}
    mock_client.get.return_value = mock_resp
    mock_client_class.return_value.__aenter__.return_value = mock_client

    with pytest.raises(HTTPException) as exc:
        await verify_token(creds)
    assert exc.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert exc.value.detail == "Invalid or expired token"
