from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from app.core.templating import templates
from app.services.user_services import register_user, get_all_users_paginated
from app.schemas.user_schemas import UserCreate
from app.core.dependencies import DbSession, ManagerOrSupervisor
from app.core.exceptions import UserAlreadyExistsError
from pydantic import ValidationError

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/", response_class = HTMLResponse)
def users_page(request: Request, current_user: ManagerOrSupervisor, session: DbSession):
    return templates.TemplateResponse("users/index.html", {"request": request})

@router.get("/list", response_class = HTMLResponse)
def users_list(request: Request, current_user: ManagerOrSupervisor, session: DbSession, page: int = 1):
    users, total_pages = get_all_users_paginated(session, page = page)
    return templates.TemplateResponse("users/partials/users_table.html", {"request": request, "users": users, "page": page, "total_pages": total_pages})

@router.get("/create", response_class = HTMLResponse)
def register_page(request: Request, current_user: ManagerOrSupervisor):
    return templates.TemplateResponse("users/register.html", {"request": request})

@router.post("/create", response_class = HTMLResponse)
def create_user(request: Request, session: DbSession, current_user: ManagerOrSupervisor, name : str = Form(...), email : str = Form(...), password : str = Form(...), role : str = Form(...)):
    form_data = {"name": name, "email": email, "role": role} 
    try:
        new_user = UserCreate(name = name, email = email, password = password, role = role)
        registered_user = register_user(session, new_user)
        return templates.TemplateResponse(
            "users/partials/register_form.html",
            {"request": request, "success": f"User {registered_user.email} registered successfully!"}
        )
    except ValidationError as e:
        error_messages = []
        print(e.errors()) # debug: print validation errors to console
        for error in e.errors():
            field = error["loc"][0] if error["loc"] else "campo"
            msg = error["msg"]
            error_messages.append(f"{field}: {msg}")
        
        return templates.TemplateResponse(
            "users/partials/register_form.html",
            {"request": request, "error": " | ".join(error_messages), **form_data}
        )
    except UserAlreadyExistsError as e:
        return templates.TemplateResponse(
            "users/partials/register_form.html",
            {"request": request, "error": str(e), **form_data}
        )
    except Exception as e:
        return templates.TemplateResponse(
            "users/partials/register_form.html",
            {"request": request, "error": f"Error inesperado: {str(e)}", **form_data}
        )