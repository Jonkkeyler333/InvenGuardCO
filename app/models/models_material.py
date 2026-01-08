from datetime import datetime, timezone
from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.models_user import User
    from models.models_bom import BomItem
    from models.models_product import ProductionConsumption

class Material(SQLModel, table = True):
    __tablename__ = "material" # type: ignore
    id : int = Field(default = None, primary_key = True)
    name : str
    unit_measure : str = Field(default = "KG")
    image_url : str | None = Field(default = None)
    reorder_threshold : float = Field(default = 0 , ge = 0)
    critical_threshold : float = Field(default = 0 , ge = 0)
    created_at : datetime = Field(default_factory = lambda : datetime.now(timezone.utc))
    inventory : "MaterialInventory" = Relationship(back_populates = "material")
    movements : list["InventoryMovement"] = Relationship(back_populates = "material")
    bom_items : list["BomItem"] = Relationship(back_populates = "material")
    consumptions : list["ProductionConsumption"] = Relationship(back_populates = "material")

class MaterialInventory(SQLModel, table = True):
    __tablename__ = "material_inventory" # type: ignore
    material_id : int = Field(default = None, primary_key = True, foreign_key = "material.id")
    quantity_avaliable : float = Field(default = 0 , ge = 0)
    last_update : datetime = Field(default_factory = lambda : datetime.now(timezone.utc))
    material : "Material" = Relationship(back_populates = "inventory")
    
class InventoryMovement(SQLModel, table = True):
    __tablename__ = "inventory_movement" # type: ignore
    id : int = Field(default = None, primary_key = True)
    material_id : int = Field(default = None, primary_key = True, foreign_key = "material.id")
    material : "Material" = Relationship(back_populates = "movements")
    quantity : float = Field(ge = 0)
    reference_type : str 
    reference_id : int | None
    created_at : datetime = Field(default_factory = lambda : datetime.now(timezone.utc))
    created_by_id : int = Field(foreign_key = "user.id")
    created_by : "User" = Relationship(back_populates = "inventory_movements")