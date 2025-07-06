import asyncio
import httpx
from tickethub.db.db import AsyncSessionLocal, engine, Base
from tickethub.models.orm import Ticket, User  
from tickethub.services.ticket_service import PRIORITY_MAP
from tickethub.config import settings

async def fetch_and_seed():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    base = settings.external_api_url
    async with httpx.AsyncClient() as client:
        todos = (await client.get(f"{base}/todos")).json()["todos"]
        # gather unique userIds
        user_ids = {t["userId"] for t in todos}
        users = {}
        for uid in user_ids:
            u = (await client.get(f"{base}/users/{uid}")).json()
            users[uid] = f"{u['firstName']} {u['lastName']}"

    async with AsyncSessionLocal() as session:
        # seed users
        session.add_all([User(id=uid, name=name) for uid, name in users.items()])
        # seed tickets
        session.add_all([
            Ticket(
                id=t["id"],
                title=t["todo"],
                status="closed" if t["completed"] else "open",
                priority=PRIORITY_MAP[t["id"] % 3],
                assignee_id=t["userId"],
                raw_json=t              
                )
            for t in todos
        ])
        await session.commit()
    print("Database seeded!")

if __name__ == "__main__":
    asyncio.run(fetch_and_seed())
