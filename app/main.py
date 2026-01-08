from fastapi import FastAPI
from app.core.config import settings
from contextlib import asynccontextmanager
from app.db.database import create_tables

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    yield
    
app = FastAPI(title="InvenGuardCO", version="0.1.0", lifespan=lifespan)

@app.get("/")
def hello_world():
    return {"message": "Hello, World"}

@app.get("/test")
def test_endpoint():
    return {"environment": settings.ENVIRONMENT,
            "database_url": settings.DATABASE.url_connection}
    