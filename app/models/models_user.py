from sqlmodel import SQLModel, Field, Relationship
from enum import Enum
from datetime import datetime, timezone
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.models_material import InventoryMovement
    from models.models_product import ProductionOrder

class UserRole(str, Enum):
    PLANT_MANAGER = "plant_manager"
    SUPERVISOR = "supervisor"
    CLERK = "clerk"
    OPERATOR = "operator"
    
class WorkUnit(SQLModel, table = True):
    __tablename__ = "work_unit" # type: ignore
    id: int = Field(default = None, primary_key = True)
    name: str
    type: str = Field(default = "production line")
    status : str = Field(default = "active")
    users : list["User"] = Relationship(back_populates = "work_unit")
    production_orders : list["ProductionOrder"] = Relationship(back_populates = "work_unit")

class User(SQLModel, table = True):
    __tablename__ = "user" # type: ignore
    id: int = Field(default = None, primary_key = True)
    name: str
    email: str = Field(unique = True)
    hash_password: str
    role : UserRole = Field(default = UserRole.OPERATOR)
    is_active: bool = Field(default = True)
    created_at : datetime = Field(default_factory = lambda : datetime.now(timezone.utc))
    work_unit_id: int | None = Field(foreign_key = "work_unit.id")
    work_unit : WorkUnit | None = Relationship(back_populates = "users")
    inventory_movements : list["InventoryMovement"] = Relationship(back_populates = "created_by")
    production_orders : list["ProductionOrder"] = Relationship(back_populates = "created_by")