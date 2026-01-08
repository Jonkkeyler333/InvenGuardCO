from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.core.config import settings
from app.core.exceptions import AppException
from contextlib import asynccontextmanager
from app.db.database import create_tables
from app.api import users

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    yield
    
app = FastAPI(title="InvenGuardCO", version="0.1.0", lifespan=lifespan)

@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )

app.include_router(users.router, prefix="/users/")

@app.get("/")
def hello_world():
    return {"message": "Hello, World"}

@app.get("/test")
def test_endpoint():
    return {"environment": settings.ENVIRONMENT,
            "database_url": settings.DATABASE.url_connection}
    