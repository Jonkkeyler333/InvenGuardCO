from fastapi import APIRouter, Request, Form, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from app.core.templating import templates
from app.services.user_services import register_user, get_all_users_paginated, update_user, get_user_by_id, delete_user as delete_service
from app.schemas.user_schemas import UserCreate, UserUpdate
from app.core.dependencies import DbSession, ManagerOrSupervisor
from app.core.exceptions import UserAlreadyExistsError, UserNotFoundError
from pydantic import ValidationError

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/", response_class = HTMLResponse)
def users_page(request: Request, current_user: ManagerOrSupervisor, session: DbSession):
    return templates.TemplateResponse("users/index.html", {"request": request})

@router.get("/list", response_class = HTMLResponse)
def users_list(request: Request, current_user: ManagerOrSupervisor, session: DbSession, page: int = 1):
    users, total_pages = get_all_users_paginated(session, page = page)
    return templates.TemplateResponse("users/partials/users_table.html", {"request": request, "users": users, "page": page, "total_pages": total_pages, "current_user": current_user})

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
            field = error["loc"][0] if error["loc"] else "field"
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
            {"request": request, "error": f"Inexpected error: {str(e)}", **form_data}
        )
        
@router.get("/{id}/edit", response_class = HTMLResponse)
def edit_user_page(request: Request, id: int, current_user: ManagerOrSupervisor, session: DbSession):
    try:
        user = get_user_by_id(session, id)
    except UserNotFoundError as e:
        return templates.TemplateResponse(
            "users/partials/edit_form.html",
            {"request": request, "error": str(e)}
        )
    return templates.TemplateResponse(
        "users/partials/edit_form.html",
        {"request": request, "user": user}
    )

@router.post("/{id}/edit", response_class = HTMLResponse)
def edit_user(request: Request, id: int, session: DbSession, current_user : ManagerOrSupervisor, name : str = Form(None), email : str = Form(None), password : str = Form(None), role : str = Form(None), is_active : bool = Form(True)):
    data_form = {"name": name, "email": email, "role": role, "is_active": is_active}
    try:
        data_user = UserUpdate(name = name, email = email, password = password, role = role, is_active = is_active)
        print(data_user)
        new_user = update_user(session, id, data_user)
        print(new_user)
        return templates.TemplateResponse(
            "users/partials/edit_form.html",
            {"request": request, "user": new_user, "success": f"User {new_user.email} updated successfully!"}
        )
    except ValidationError as e:
        error_messages = []
        for error in e.errors():
            field = error["loc"][0] if error["loc"] else "field"
            msg = error["msg"]
            error_messages.append(f"{field}: {msg}")
        return templates.TemplateResponse(
            "users/partials/edit_form.html",
            {"request": request, "error": " | ".join(error_messages), "user": data_form}
        )
    except UserNotFoundError as e:
        return templates.TemplateResponse(
            "users/partials/edit_form.html",
            {"request": request, "error": str(e), "user": data_form}
        )
    except UserAlreadyExistsError as e:
        return templates.TemplateResponse(
            "users/partials/edit_form.html",
            {"request": request, "error": str(e), "user": data_form}
        )
        
@router.delete("/{id}", response_class = HTMLResponse)
def delete_user(request: Request, id: int, session: DbSession, current_user : ManagerOrSupervisor):
    result = delete_service(session, id)
    if result:
            response = Response(status_code = 201)
            response.headers["HX-Trigger"] = "userDeleted"
            return response
    else:
        response = Response(status_code = 404)
        response.headers["HX-Trigger"] = "userDeleted"
        return response