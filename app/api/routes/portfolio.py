from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/portfolio", response_class=HTMLResponse)
async def read_portfolio(request: Request):
    return templates.TemplateResponse("portfolio.html", {"request": request})
