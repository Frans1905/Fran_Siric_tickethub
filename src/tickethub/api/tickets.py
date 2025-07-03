from fastapi import APIRouter, Query, HTTPException
from tickethub.services.ticket_service import fetch_tickets, fetch_ticket_by_id
from tickethub.models.ticket import TicketResponse, TicketWithSource
from typing import List, Optional
import httpx

router = APIRouter()

@router.get("/", response_model=List[TicketResponse])
async def list_tickets(
    status: Optional[str] = Query(None, regex="^(open|closed)$"),
    priority: Optional[str] = Query(None, regex="^(low|medium|high)$"),
    limit: Optional[int] = None
):
    tickets = await fetch_tickets()
    # Filter
    if status:
        tickets = [t for t in tickets if t.status == status]
    if priority:
        tickets = [t for t in tickets if t.priority == priority]
    if limit:
        tickets = tickets[:limit]

    return tickets


@router.get("/search", response_model=List[TicketResponse])
async def search_tickets(
    q: Optional[str] = Query(None, min_length=1),
    limit: Optional[int] = None
):
    tickets = await fetch_tickets()
    if q:
        tickets = [t for t in tickets if q.lower() in t.title.lower()]

    if limit:
        tickets = tickets[:limit]

    return tickets
   

@router.get("/{ticket_id}", response_model=TicketWithSource)
async def get_ticket_details(ticket_id: int):
    try:
        return await fetch_ticket_by_id(ticket_id)
    except httpx.HTTPStatusError:
        raise HTTPException(status_code=404, detail="Ticket not found")


