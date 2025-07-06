from tickethub.models.orm import Ticket as TicketORM
from sqlalchemy import select
from tickethub.db.db import AsyncSessionLocal
from tickethub.models.ticket import TicketResponse, TicketWithSource
from fastapi import HTTPException
from sqlalchemy.orm import selectinload
from tickethub.config import settings
from tickethub.services.cache import redis_client
import json
import logging

logger = logging.getLogger(__name__)

PRIORITY_MAP = {0: "low", 1: "medium", 2: "high"}
CACHE_TTL = settings.cache_ttl
CACHING_ENABLED = settings.caching_enabled

async def fetch_tickets():
    logger.info("Fetching all tickets")
    cache_key = "tickets:all"
    if (CACHING_ENABLED):
        cached = await redis_client.get(cache_key)
        if cached:
            logger.debug("Tickets fetched from Redis cache")
            data = json.loads(cached)
            return [TicketResponse(**t) for t in data] 


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

    if (CACHING_ENABLED):
        await redis_client.setex(cache_key, CACHE_TTL, json.dumps([ticket.dict() for ticket in tickets]))
        logger.debug("Tickets stored in Redis cache")
    return tickets

async def fetch_ticket_stats():
    logger.info("Fetching ticket stats")
    cache_key = "tickets:stats"
    if (CACHING_ENABLED):
        cached = await redis_client.get(cache_key)
        if cached:
            logger.debug("Ticket stats fetched from Redis cache")
            return json.loads(cached)

    async with AsyncSessionLocal() as session:
        result = await session.execute(select(TicketORM))
        tickets = result.scalars().all()

    stats = {
        "total": len(tickets),
        "open": 0,
        "closed": 0,
        "priority": {"low": 0, "medium": 0, "high": 0},
    }

    for ticket in tickets:
        stats[ticket.status] += 1
        stats["priority"][ticket.priority] += 1

    if (CACHING_ENABLED):
        await redis_client.setex(cache_key, CACHE_TTL, json.dumps(stats))
        logger.debug("Ticket stats stored in Redis cache")
    return stats

async def fetch_ticket_by_id(ticket_id: int) -> TicketWithSource:
    logger.info(f"Fetching ticket with ID {ticket_id}")
    cache_key = f"ticket:{ticket_id}"

    if (CACHING_ENABLED):
        cached = await redis_client.get(cache_key)
        if cached:
            logger.debug(f"Ticket {ticket_id} fetched from Redis cache")
            return TicketWithSource(**json.loads(cached))

    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(TicketORM).where(TicketORM.id == ticket_id).options(selectinload(TicketORM.assignee))
        )
        ticket = result.scalar_one_or_none()
    
    if ticket is None:
        logger.warning(f"Ticket with ID {ticket_id} not found.")
        raise HTTPException(status_code=404, detail="Ticket not found")

    logger.debug(f"Found ticket: {ticket.id} - {ticket.title}")
    ticket_data = TicketWithSource(
        id=ticket.id,
        title=ticket.title,
        status=ticket.status,
        priority=ticket.priority,
        assignee=ticket.assignee.name,
        source=ticket.raw_json,
    )

    if (CACHING_ENABLED):
        await redis_client.setex(cache_key, CACHE_TTL, json.dumps(ticket_data.model_dump()))
        logger.debug(f"Ticket {ticket_id} stored in Redis cache")

    return ticket_data

