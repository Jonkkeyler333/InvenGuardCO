from sqlmodel import Session
from app.db.database import engine
from app.models.models_user import User, UserRole
from app.core.security import verify_access_token
from app.core.exceptions import InvalidCredentialsError
from fastapi import Depends, Request, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated, Optional

def get_session():
    """Generador de sesión de base de datos"""
    with Session(engine) as session:
        yield session
        
DbSession = Annotated[Session, Depends(get_session)]

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token", auto_error=False)

def get_token_from_cookie(request: Request) -> Optional[str]:
    """
    Extrae el token de acceso desde la cookie.
    Usado para autenticación en vistas web (templates HTML).
    """
    return request.cookies.get("access_token")

def get_current_user(request: Request, session: Session = Depends(get_session), token_from_header: Optional[str] = Depends(oauth2_scheme)) -> User:
    """
    Obtiene el usuario actual desde el token JWT.
    
    Busca el token en dos lugares (en orden de prioridad):
    1. Header Authorization: Bearer <token> (para APIs)
    2. Cookie 'access_token' (para vistas web/HTMX)
    
    Raises:
        HTTPException 401: Si no hay token o es inválido
    """
    # Prioridad: Header > Cookie
    token = token_from_header or get_token_from_cookie(request)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )
    try:
        user_id = verify_access_token(token)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )
    user = session.get(User, int(user_id))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inactivo"
        )
    return user

class RoleChecker:
    """
    Clase que verifica si el usuario tiene uno de los roles permitidos.
    
    Uso:
        require_manager = RoleChecker([UserRole.PLANT_MANAGER])
        
        @router.post("/users")
        def create_user(user: Annotated[User, Depends(require_manager)]):
            ...
    """
    def __init__(self, allowed_roles: list[UserRole]):
        self.allowed_roles = allowed_roles
    
    def __call__(self, current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in self.allowed_roles:
            raise HTTPException(
                status_code = status.HTTP_403_FORBIDDEN,
                detail = f"Forbidden !!"
            )
        return current_user

require_plant_manager = RoleChecker([UserRole.PLANT_MANAGER])
require_supervisor = RoleChecker([UserRole.SUPERVISOR])
require_manager_or_supervisor = RoleChecker([UserRole.PLANT_MANAGER, UserRole.SUPERVISOR])
require_clerk_or_higher = RoleChecker([UserRole.PLANT_MANAGER, UserRole.SUPERVISOR, UserRole.CLERK])

CurrentUser = Annotated[User, Depends(get_current_user)]

PlantManager = Annotated[User, Depends(require_plant_manager)]
Supervisor = Annotated[User, Depends(require_supervisor)]
ManagerOrSupervisor = Annotated[User, Depends(require_manager_or_supervisor)]
ClerkOrHigher = Annotated[User, Depends(require_clerk_or_higher)]