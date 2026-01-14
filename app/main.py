from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.core.config import settings
from app.core.exceptions import AppException
from contextlib import asynccontextmanager
from app.db.database import create_tables
from fastapi.staticfiles import StaticFiles
from app.web import auth as web_auth
from app.web import users, dashboard
from app.core.templating import templates

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

app.include_router(web_auth.router)
app.include_router(users.router)
app.include_router(dashboard.router)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/test")
def test_endpoint():
    return {"environment": settings.ENVIRONMENT,
            "database_url": settings.DATABASE.url_connection}
    