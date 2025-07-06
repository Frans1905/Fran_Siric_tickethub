from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from tickethub.api import tickets, auth, doc
from tickethub.db.db import Base, engine
import logging
from tickethub.config import settings
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

log_level = getattr(logging, settings.log_level.upper(), logging.INFO)

logging.basicConfig(
    level=log_level,      
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

limiter = Limiter(key_func=get_remote_address, default_limits=[settings.rate_limit])

app = FastAPI(title="TicketHub", version="0.1.0")

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(SlowAPIMiddleware)

app.include_router(tickets.router, prefix="/tickets", tags=["Tickets"])
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])

app.mount("/static", StaticFiles(directory="src/static"), name="static")

app.include_router(doc.router)

@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "ok"}
