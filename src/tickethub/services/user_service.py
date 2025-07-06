from tickethub.config import settings
import httpx

async def get_username_by_id(user_id: int) -> str:
    base = settings.external_api_url
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{base}/users/{user_id}")
        data = resp.json()
    return f"{data['firstName']} {data['lastName']}"
