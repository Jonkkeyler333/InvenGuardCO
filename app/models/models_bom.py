from datetime import datetime, timezone
from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from app.models.models_product import Product
    from app.models.models_material import Material

class Bom(SQLModel, table = True):
    __tablename__ = "bom" # type: ignore
    id : int = Field(default = None, primary_key = True)
    product_id : int = Field(foreign_key = "product.id")
    product : "Product" = Relationship(back_populates = "bom")
    version : int = Field(default = 1, ge = 1)
    created_at : datetime = Field(default_factory = lambda : datetime.now(timezone.utc))
    items : list["BomItem"] = Relationship(back_populates = "bom")

class BomItem(SQLModel, table = True):
    __tablename__ = "bom_item" # type: ignore
    id : int = Field(default = None, primary_key = True)
    quantity_required : float = Field(ge = 0)
    bom_id : int = Field(foreign_key = "bom.id")
    bom : "Bom" = Relationship(back_populates = "items")
    material_id : int = Field(foreign_key = "material.id")
    material : "Material" = Relationship(back_populates = "bom_items")