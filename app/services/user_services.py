from sqlmodel import Session
from app.repositories.user_repository import UserRepository
from app.core.security import hash_password, verify_password, create_access_token
from app.schemas.user_schemas import UserCreate, UserRead, UserLogin, TokenResponse
from app.core.exceptions import UserAlreadyExistsError, InvalidCredentialsError
from typing import Tuple

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

def authenticate_user(session: Session, user_login: UserLogin) -> TokenResponse:
    user_repo = UserRepository(session)
    user_db = user_repo.get_user_by_email(user_login.email)
    if not user_db:
        raise InvalidCredentialsError()
    if not verify_password(user_login.password, user_db.hash_password):
        raise InvalidCredentialsError()
    token = create_access_token(str(user_db.id)) # type: ignore
    return TokenResponse(access_token = token)

def get_all_users_paginated(session: Session, page : int = 1, limit: int = 10) -> Tuple[list[UserRead], int]:
    user_repo = UserRepository(session)
    users, total_pages = user_repo.get_all_users(page = page, limit = limit)
    return [UserRead.model_validate(user) for user in users], total_pages