from fastapi import APIRouter
from app.services.user_services import register_user
from app.core.dependencies import DbSession, CurrentUser
from app.schemas.user_schemas import UserCreate, UserRead

router = APIRouter(prefix="/users-old", tags=["users"])

@router.post("",response_model=UserRead, status_code=201, responses={
        409: {
            "description": "User already exists",
            "content": {
                "application/json": {
                    "example": {"detail": "User with email 'x@mail.com' already exists"}
                }
            }
        }
    }
)
def create_user(user_create: UserCreate, session: DbSession):
    """
    Register a new user.
    
    - **name**: User's full name
    - **email**: User's email address
    - **password**: User's password
    - **role**: User role (optional)
    """
    return register_user(session, user_create)


@router.get("/me", response_model = UserRead)
def get_current_user_info(current_user: CurrentUser):
    """
    Get current authenticated user's profile.
    """
    return current_user