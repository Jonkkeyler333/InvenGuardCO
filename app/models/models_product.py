from datetime import datetime, timezone
from sqlmodel import SQLModel, Field, Relationship
from enum import Enum
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from app.models.models_bom import Bom
    from app.models.models_user import WorkUnit, User
    from app.models.models_material import Material
    
class OrderStatus(str, Enum):
    PENDING = "pending"
    IN_PRODUCTION = "in_production"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class Product(SQLModel, table = True):
    __tablename__ = "product" # type: ignore
    id : int = Field(default = None, primary_key = True)
    name : str
    description : str | None = Field(default = None)
    sku : str = Field(unique = True)
    image_url : str | None = Field(default = None)
    is_active : bool = Field(default = True)
    created_at : datetime = Field(default_factory = lambda : datetime.now(timezone.utc))
    bom : "Bom" = Relationship(back_populates = "product")    
    production_orders : list["ProductionOrder"] = Relationship(back_populates = "product")

class ProductionOrder(SQLModel, table = True):
    __tablename__ = "production_order" # type: ignore
    id : int = Field(default = None, primary_key = True)
    product_id : int = Field(foreign_key = "product.id")
    product : "Product" = Relationship(back_populates = "production_orders")
    quantity_produce : float = Field(ge = 1)
    status : OrderStatus = Field(default = OrderStatus.PENDING)
    created_at : datetime = Field(default_factory = lambda : datetime.now(timezone.utc))
    started_at : datetime | None = Field(default = None)
    completed_at : datetime | None = Field(default = None)
    work_unit_id : int | None = Field(default = None, foreign_key = "work_unit.id")
    work_unit : Optional["WorkUnit"] = Relationship(back_populates = "production_orders")
    created_by_id : int | None = Field(default = None, foreign_key = "user.id")
    created_by : Optional["User"] = Relationship(back_populates = "production_orders")
    consumptions : list["ProductionConsumption"] = Relationship(back_populates = "production_order")
    
class ProductionConsumption(SQLModel, table = True):
    __tablename__ = "production_consumption" # type: ignore
    id : int = Field(default = None, primary_key = True)
    production_order_id : int = Field(foreign_key = "production_order.id")
    production_order : "ProductionOrder" = Relationship(back_populates = "consumptions")
    material_id : int = Field(foreign_key = "material.id")
    material : "Material" = Relationship(back_populates = "consumptions")
    quantity_bom : float = Field(ge = 0)
    quantity_consumed : float = Field(ge = 0, default = 0)
    created_at : datetime = Field(default_factory = lambda : datetime.now(timezone.utc))