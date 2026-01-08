from sqlmodel import Session
from app.repositories.user_repository import UserRepository
from app.core.security import hash_password, verify_password
from app.schemas.user_schemas import UserCreate, UserRead
from app.core.exceptions import UserAlreadyExistsError, UserNotFoundError, InvalidCredentialsError

def register_user(session: Session, user_create: UserCreate) -> UserRead:
    user_repo = UserRepository(session)
    user_db = user_repo.get_user_by_email(user_create.email)
    if user_db:
        raise UserAlreadyExistsError(user_create.email)
    hashed_pw = hash_password(user_create.password)
    user = user_repo.create_user(name = user_create.name, 
                                 email = user_create.email,
                                 hash_password = hashed_pw,
                                 role = user_create.role) # type: ignore
    created_user = UserRead.model_validate(user)
    return created_user