
from fastapi import APIRouter, Query
from tickethub.services.ticket_service import fetch_tickets
from tickethub.models.ticket import TicketResponse
from typing import List, Optional

router = APIRouter()

@router.get("/", response_model=List[TicketResponse])
async def list_tickets(
    status: Optional[str] = Query(None, regex="^(open|closed)$"),
    priority: Optional[str] = Query(None, regex="^(low|medium|high)$"),
    q: Optional[str] = None,
    skip: int = 0,
    limit: int = 10
):
    tickets = await fetch_tickets()
    # Filter
    if status:
        tickets = [t for t in tickets if t.status == status]
    if priority:
        tickets = [t for t in tickets if t.priority == priority]
    if q:
        tickets = [t for t in tickets if q.lower() in t.title.lower()]
    return tickets[skip:skip + limit]
