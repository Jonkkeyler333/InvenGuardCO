from fastapi import APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from app.services.user_services import authenticate_user
from app.core.dependencies import DbSession
from app.schemas.user_schemas import TokenResponse, UserLogin

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=TokenResponse, responses={
        401: {
            "description": "Invalid credentials",
            "content": {
                "application/json": {
                    "example": {"detail": "Invalid email or password"}
                }
            }
        }
    }
)
def login(credentials: UserLogin, session: DbSession):
    """
    Authenticate user and return access token.
    
    - **email**: User's email address
    - **password**: User's password
    - **Returns**: Access token for authenticated requests
    """
    return authenticate_user(session, credentials)
