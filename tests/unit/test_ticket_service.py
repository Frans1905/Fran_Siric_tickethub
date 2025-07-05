import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from fastapi import HTTPException

from tickethub.services.ticket_service import fetch_tickets, fetch_ticket_by_id
from tickethub.models.orm import Ticket as TicketORM
from tickethub.models.ticket import TicketResponse, TicketWithSource


@pytest.mark.asyncio
@patch("tickethub.services.ticket_service.AsyncSessionLocal")
async def test_fetch_tickets(mock_session_local):
    # Create mock ticket with mocked assignee
    mock_ticket = TicketORM(id=1, title="Test Ticket", status="open", priority="high")
    mock_ticket.assignee = MagicMock()
    mock_ticket.assignee.name = "Alice"

    # Set up mocks
    mock_scalars = MagicMock()
    mock_scalars.all.return_value = [mock_ticket]

    mock_result = MagicMock()
    mock_result.scalars.return_value = mock_scalars

    mock_session = AsyncMock()
    mock_session.execute.return_value = mock_result
    mock_session_local.return_value.__aenter__.return_value = mock_session

    # Run
    result = await fetch_tickets()

    # Assert
    assert isinstance(result, list)
    assert isinstance(result[0], TicketResponse)
    assert result[0].title == "Test Ticket"
    assert result[0].assignee == "Alice"


@pytest.mark.asyncio
@patch("tickethub.services.ticket_service.AsyncSessionLocal")
async def test_fetch_ticket_by_id_success(mock_session_local):
    # Create mock ticket
    mock_ticket = TicketORM(id=1, title="Test Ticket", status="open", priority="medium")
    mock_ticket.assignee = MagicMock()
    mock_ticket.assignee.name = "Bob"
    mock_ticket.raw_json = {"mock": "json"}

    # Setup mocks
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = mock_ticket

    mock_session = AsyncMock()
    mock_session.execute.return_value = mock_result
    mock_session_local.return_value.__aenter__.return_value = mock_session

    # Run
    result = await fetch_ticket_by_id(1)

    # Assert
    assert isinstance(result, TicketWithSource)
    assert result.id == 1
    assert result.assignee == "Bob"
    assert result.source == {"mock": "json"}


@pytest.mark.asyncio
@patch("tickethub.services.ticket_service.AsyncSessionLocal")
async def test_fetch_ticket_by_id_not_found(mock_session_local):
    # Setup to return None
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = None

    mock_session = AsyncMock()
    mock_session.execute.return_value = mock_result
    mock_session_local.return_value.__aenter__.return_value = mock_session

    # Run and assert exception
    with pytest.raises(HTTPException) as exc_info:
        await fetch_ticket_by_id(999)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Ticket not found"
