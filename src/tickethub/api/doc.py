from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from pathlib import Path

router = APIRouter(tags=["docs"])

@router.get("/redoc-static", include_in_schema=False)
async def redoc_static():
    html_path = Path("static/redoc.html")
    if not html_path.exists():
        return HTMLResponse(content="Redoc HTML not found.", status_code=404)
    return HTMLResponse(content=html_path.read_text(), status_code=200)
