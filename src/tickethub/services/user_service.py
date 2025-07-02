
import httpx
from functools import lru_cache

@lru_cache(maxsize=1000)
async def get_username_by_id(user_id: int) -> str:
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"https://dummyjson.com/users/{user_id}")
        data = resp.json()
    return f"{data['firstName']} {data['lastName']}"
