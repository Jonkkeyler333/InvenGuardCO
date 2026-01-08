from sqlmodel import create_engine, Session, SQLModel
from app.core.config import settings

DATABASE_URL = settings.DATABASE.url_connection
engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session

def create_tables():
    from app.models import models_user, models_material, models_product, models_bom
    SQLModel.metadata.create_all(engine)