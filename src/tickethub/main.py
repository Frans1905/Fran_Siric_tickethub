
from fastapi import FastAPI
from tickethub.api import tickets
from tickethub.db.db import Base, engine
import logging

logging.basicConfig(
    level=logging.INFO,      
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

app = FastAPI(title="TicketHub", version="0.1.0")

app.include_router(tickets.router, prefix="/tickets", tags=["Tickets"])
@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "ok"}
