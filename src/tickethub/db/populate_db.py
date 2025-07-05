import asyncio
import httpx
from tickethub.db.db import AsyncSessionLocal, engine, Base
from tickethub.models.orm import Ticket, User  
from tickethub.services.ticket_service import PRIORITY_MAP

async def fetch_and_seed():
    # 1) create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # 2) fetch todos & users
    async with httpx.AsyncClient() as client:
        todos = (await client.get("https://dummyjson.com/todos")).json()["todos"]
        # gather unique userIds
        user_ids = {t["userId"] for t in todos}
        users = {}
        for uid in user_ids:
            u = (await client.get(f"https://dummyjson.com/users/{uid}")).json()
            users[uid] = f"{u['firstName']} {u['lastName']}"

    # 3) insert into DB
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
                raw_json=t  # if you store raw JSON too
            )
            for t in todos
        ])
        await session.commit()
    print("Database seeded!")

if __name__ == "__main__":
    asyncio.run(fetch_and_seed())
