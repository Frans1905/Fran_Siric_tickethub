
from fastapi import FastAPI
from tickethub.api import tickets

app = FastAPI(title="TicketHub", version="0.1.0")

app.include_router(tickets.router, prefix="/tickets", tags=["Tickets"])

@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "ok"}
