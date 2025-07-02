import asyncio
import httpx
from .user_service import get_username_by_id
from tickethub.models.ticket import TicketResponse, TicketWithSource

PRIORITY_MAP = {0: "low", 1: "medium", 2: "high"}

async def fetch_tickets():
    async with httpx.AsyncClient() as client:
        resp = await client.get("https://dummyjson.com/todos")
        data = resp.json()["todos"]
    '''
    coroutines = [get_username_by_id(todo["userId"]) for todo in data]
    assignees = await asyncio.gather(*coroutines)
    '''

    tickets = []
    users = {}
    for item in data:
        status = "closed" if item["completed"] else "open"
        priority = PRIORITY_MAP[item["id"] % 3]
        assignee = None
        if (item["userId"] in users.keys()):
            assignee = users[item["userId"]]
        else:
            assignee = await get_username_by_id(item["userId"])
            users[item["userId"]] = assignee
        tickets.append(TicketResponse(
            id=item["id"],
            title=item["todo"],
            status=status,
            priority=priority,
            assignee=assignee,
        ))
    return tickets


async def fetch_ticket_by_id(ticket_id: int) -> TicketWithSource:
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"https://dummyjson.com/todos/{ticket_id}")
        resp.raise_for_status()
        raw = resp.json()

    status = "closed" if raw["completed"] else "open"
    priority = PRIORITY_MAP[raw["id"] % 3]
    assignee = await get_username_by_id(raw["userId"])

    return TicketWithSource(
        id=raw["id"],
        title=raw["todo"],
        status=status,
        priority=priority,
        assignee=assignee,
        source=raw,
    )
