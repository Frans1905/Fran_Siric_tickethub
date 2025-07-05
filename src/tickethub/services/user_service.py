
import httpx

async def get_username_by_id(user_id: int) -> str:
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"https://dummyjson.com/users/{user_id}")
        data = resp.json()
    return f"{data['firstName']} {data['lastName']}"
