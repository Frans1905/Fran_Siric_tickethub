from fastapi import APIRouter, HTTPException
from tickethub.models.login import LoginRequest, LoginResponse
from tickethub.services.auth_service import get_token
import logging
import httpx

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/login", response_model=LoginResponse)
async def login_dummyjson(data: LoginRequest):
    logger.info(f"User {data.dict()['username']} trying to log in")

    try:
        token = await get_token(data.dict()["username"], data.dict()["password"])

    except httpx.HTTPStatusError:
        logger.warning(f"User {data.dict()['username']} could not be logged in")
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return token


