from typing import Any
from pydantic import BaseModel, Field

class TicketResponse(BaseModel):
    id: int
    title: str
    status: str
    priority: str
    assignee: str

class TicketWithSource(TicketResponse):
    source: dict[str, Any]
