from fastapi import APIRouter, Query, HTTPException
from tickethub.services.ticket_service import fetch_tickets, fetch_ticket_by_id, fetch_ticket_stats
from tickethub.models.ticket import TicketResponse, TicketWithSource
from typing import List, Optional
import httpx
import logging

router = APIRouter()

logger = logging.getLogger(__name__)

@router.get("/", response_model=List[TicketResponse])
async def list_tickets(
    status: Optional[str] = Query(None, pattern="^(open|closed)$"),
    priority: Optional[str] = Query(None, pattern="^(low|medium|high)$"),
    limit: Optional[int] = None
):
    logger.info(f"Listing tickets with status={status}, priority={priority}, limit={limit}")
    tickets = await fetch_tickets()
    # Filter
    if status:
        tickets = [t for t in tickets if t.status == status]
    if priority:
        tickets = [t for t in tickets if t.priority == priority]
    if limit:
        tickets = tickets[:limit]

    logger.debug(f"Returning {len(tickets)} tickets after filtering.")
    return tickets


@router.get("/search", response_model=List[TicketResponse])
async def search_tickets(
    q: Optional[str] = Query(None, min_length=1),
    limit: Optional[int] = None
):
    logger.info(f"Searching tickets with query='{q}' and limit={limit}")
    tickets = await fetch_tickets()
    if q:
        tickets = [t for t in tickets if q.lower() in t.title.lower()]

    if limit:
        tickets = tickets[:limit]

    logger.debug(f"Found {len(tickets)} matching tickets.")
    return tickets

@router.get("/stats")
async def get_ticket_stats():
    logger.info("Fetching ticket statistics")
    stats = await fetch_ticket_stats() 
    return stats
  

@router.get("/{ticket_id}", response_model=TicketWithSource)
async def get_ticket_details(ticket_id: int):
    logger.info(f"Fetching ticket details for ID {ticket_id}")
    try:
        ticket = await fetch_ticket_by_id(ticket_id)
        logger.debug(f"Ticket found: {ticket.title}")
        return ticket
    except httpx.HTTPStatusError as e:
        logger.warning(f"Ticket with ID {ticket_id} not found: {e}")
        raise HTTPException(status_code=404, detail="Ticket not found")


