from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import datetime

class MaterialBase(BaseModel):
    name: str
    sku: str
    unit_measure: str 
    reorder_threshold: float = Field(default = 0 , ge = 0)
    critical_threshold: float = Field(default = 0 , ge = 0)
    image_url: str | None = None

class MaterialCreate(MaterialBase):
    pass

class MaterialUpdate(BaseModel):
    name: str | None = None
    sku: str | None = None
    unit_measure: str | None = None
    reorder_threshold: float | None = None
    critical_threshold: float | None = None
    image_url: str | None = None

class MaterialRead(MaterialBase):
    id: int
    is_active: bool = True
    created_at: datetime | None = None
    inventory: Optional["MaterialInventoryRead"] = None
    model_config = ConfigDict(from_attributes = True)

class MaterialInventoryRead(BaseModel):
    material_id: int
    quantity_available: float
    last_update: datetime | None = None
    model_config = ConfigDict(from_attributes = True)
    
class CreateMovementBase(BaseModel):
    material_id: int
    quantity: float = Field(default = 0 ,ge = 0)
    created_by_id: int
    reference_id: int | None = None
    reference_type: str = "Entry"
    
class InventoryMovementRead(CreateMovementBase):
    id: int
    created_at: datetime | None = None
    model_config = ConfigDict(from_attributes = True)