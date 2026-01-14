from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from app.core.templating import templates
from app.services.user_services import authenticate_user
from app.schemas.user_schemas import UserLogin
from app.core.dependencies import DbSession
from app.core.exceptions import InvalidCredentialsError

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    """Página de login completa"""
    return templates.TemplateResponse("auth/login.html", {"request": request})


@router.post("/login", response_class = HTMLResponse)
def login_submit(request: Request, session: DbSession, email: str = Form(...), password: str = Form(...)):
    """
    Procesa el login - Soporta tanto HTMX como peticiones normales.
    
    HTMX envía el header 'HX-Request' en sus peticiones.
    - Si es HTMX: devuelve fragmento HTML parcial
    - Si es normal: devuelve página completa o redirección
    """
    credentials = UserLogin(email = email, password = password)
    is_htmx = request.headers.get("HX-Request") == "true"
    
    try:
        token_response = authenticate_user(session, credentials)
        if is_htmx:
            # HTMX: Redirigir usando header especial HX-Redirect
            response = HTMLResponse(content="")
            response.headers["HX-Redirect"] = "/dashboard"
        else:
            # Normal: Redirección HTTP estándar
            response = RedirectResponse(url="/dashboard", status_code=302)
        response.set_cookie(
            key = "access_token",
            value = token_response.access_token,
            httponly = True,  # No accesible desde JavaScript
            secure = False,   # Cambiar a True en producción con HTTPS
            samesite = "lax"
        )
        return response
        
    except InvalidCredentialsError as e:
        if is_htmx:
            # HTMX: Devolver solo el fragmento del formulario con error
            return templates.TemplateResponse(
                "auth/partials/login_form.html",
                {"request": request, "error": str(e), "email": email}
            )
        else:
            return templates.TemplateResponse(
                "auth/login.html",
                {"request": request, "error": str(e)}
            )


@router.get("/logout")
def logout(request: Request):
    """Cerrar sesión eliminando la cookie"""
    response = RedirectResponse(url="/auth/login", status_code=302)
    response.delete_cookie(key="access_token")
    return response