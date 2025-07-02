
from pydantic import BaseModel, Field

class TicketResponse(BaseModel):
    id: int
    title: str
    status: str
    priority: str
    assignee: str
