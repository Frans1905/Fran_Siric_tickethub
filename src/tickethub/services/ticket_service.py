
import httpx
from .user_service import get_username_by_id
from tickethub.models.ticket import TicketResponse

PRIORITY_MAP = {0: "low", 1: "medium", 2: "high"}

async def fetch_tickets():
    async with httpx.AsyncClient() as client:
        resp = await client.get("https://dummyjson.com/todos")
        data = resp.json()["todos"]

    tickets = []
    for item in data:
        status = "closed" if item["completed"] else "open"
        priority = PRIORITY_MAP[item["id"] % 3]
        assignee = await get_username_by_id(item["userId"])
        tickets.append(TicketResponse(
            id=item["id"],
            title=item["todo"],
            status=status,
            priority=priority,
            assignee=assignee,
        ))
    return tickets
