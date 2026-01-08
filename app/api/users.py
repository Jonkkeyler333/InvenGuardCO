from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from app.core.exceptions import AppException
from app.services.user_services import register_user
from app.core.dependencies import DbSession
from app.schemas.user_schemas import UserCreate, UserRead

router = APIRouter(tags = ["users"])

@router.post("/register/", response_model=UserRead)
def register_user_endpoint(user_create: UserCreate, session: DbSession):
    user = register_user(session, user_create)
    return user