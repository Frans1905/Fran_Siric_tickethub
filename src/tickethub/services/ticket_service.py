from tickethub.models.orm import Ticket as TicketORM
from sqlalchemy import select
from tickethub.db.db import AsyncSessionLocal
from tickethub.models.ticket import TicketResponse, TicketWithSource
from sqlalchemy.orm import selectinload
from fastapi import HTTPException
import logging

logger = logging.getLogger(__name__)

PRIORITY_MAP = {0: "low", 1: "medium", 2: "high"}

async def fetch_tickets():
    logger.info("Fetching all tickets")
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(TicketORM).options(selectinload(TicketORM.assignee)))
        tickets_orm = result.scalars().all()

    tickets = []
    for item in tickets_orm:
       tickets.append(TicketResponse(
            id=item.id,
            title=item.title,
            status=item.status,
            priority=item.priority,
            assignee=item.assignee.name,
        ))

    return tickets


async def fetch_ticket_by_id(ticket_id: int) -> TicketWithSource:
    logger.info(f"Fetching ticket with ID {ticket_id}")
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(TicketORM).where(TicketORM.id == ticket_id).options(selectinload(TicketORM.assignee))
        )
        ticket = result.scalar_one_or_none()
    
    if ticket is None:
        logger.warning(f"Ticket with ID {ticket_id} not found.")
        raise HTTPException(status_code=404, detail="Ticket not found")

    logger.debug(f"Found ticket: {ticket.id} - {ticket.title}")
    return TicketWithSource(
        id=ticket.id,
        title=ticket.title,
        status=ticket.status,
        priority=ticket.priority,
        assignee=ticket.assignee.name,
        source=ticket.raw_json,
    )
