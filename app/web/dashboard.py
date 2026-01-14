from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from app.core.templating import templates
from app.core.dependencies import DbSession, CurrentUser

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

@router.get("/", response_class=HTMLResponse)
def dashboard_page(request: Request, current_user: CurrentUser):
    return templates.TemplateResponse("dashboard/dashboard.html", {"request": request, "current_user": current_user})