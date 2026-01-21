from app.models.models_material import Material, MaterialInventory, InventoryMovement, MoveType
from sqlmodel import Session, select, func, col
from math import ceil
from typing import Tuple
from datetime import datetime, timezone

class MaterialRepository:
    def __init__(self, session: Session):
        self.session = session
    
    def create_material(self, name: str, sku: str, unit_measure: str = "KG", image_url: str | None = None,reorder_threshold: float = 0, critical_threshold: float = 0) -> Material:
        new_material = Material(name = name, 
                                unit_measure = unit_measure, 
                                sku = sku,
                                image_url = image_url, 
                                reorder_threshold = reorder_threshold, 
                                critical_threshold = critical_threshold)
        self.session.add(new_material)
        self.session.commit()
        self.session.refresh(new_material)
        inventory = MaterialInventory(material_id = new_material.id) # initialize in 0 , cause the material has just been created , don't know about movements yet
        self.session.add(inventory)
        self.session.commit()
        return new_material
    
    def get_material_by_id(self, material_id: int) -> Material | None:
        statement = select(Material).where(Material.id == material_id)
        material = self.session.exec(statement).first()
        return material # we can get inventory by material.inventory
    
    def get_material_by_sku(self, sku: str) -> Material | None:
        statement = select(Material).where(Material.sku == sku)
        material = self.session.exec(statement).first()
        return material
    
    def get_all_material(self, page : int = 1, limit: int = 10) -> Tuple[list[Material], int]:
        offset = (page - 1) * limit
        statement = select(Material).offset(offset).limit(limit).order_by(col(Material.id))
        results = self.session.exec(statement).all()
        total = self.session.exec(select(func.count(col(Material.id)))).one()
        total_pages = ceil(total / limit)
        return list(results), total_pages
    
    def get_all_material_inventory(self, page : int = 1, limit: int = 10, desc: bool = False) -> Tuple[list[Material], int]:
        offset = (page - 1) * limit
        statement = (select(Material)
                     .join(MaterialInventory)
                     .offset(offset)
                     .limit(limit)
                     .order_by(col(MaterialInventory.quantity_available).desc() if desc else col(MaterialInventory.quantity_available).asc()))
        results = self.session.exec(statement).all()
        total = self.session.exec(select(func.count(col(Material.id)))).one()
        total_pages = ceil(total / limit)
        return list(results), total_pages
    
    def get_critical_inventory_materials(self, desc: bool = False) -> list[Material]:
        statement = (select(Material)
                     .join(MaterialInventory)
                     .where(MaterialInventory.quantity_available <= Material.critical_threshold)
                     .order_by(col(MaterialInventory.quantity_available).desc() if desc else col(MaterialInventory.quantity_available).asc()))
        results = self.session.exec(statement).all()
        return list(results)
    
    def update_material(self, material_id: int, **kwargs) -> Material | None:
        material_db = self.session.get(Material, material_id)
        if not material_db:
            return None
        for key, value in kwargs.items():
            if hasattr(material_db, key) and value is not None:
                setattr(material_db, key, value)
        self.session.commit()
        self.session.refresh(material_db)
        return material_db
    
    def delete_material(self, material_id: int) -> bool:
        material_db = self.session.get(Material, material_id)
        if not material_db:
            return False
        self.session.delete(material_db)
        self.session.commit()
        return True
    
    def lock_inventory_row(self, material_id: int) -> MaterialInventory | None:
        statement = select(MaterialInventory).where(MaterialInventory.material_id == material_id).with_for_update()
        inventory = self.session.exec(statement).first()
        return inventory
    
    def update_inventory_quantity(self, inventory: MaterialInventory, new_quantity: float):
        inventory.quantity_available = new_quantity
        inventory.last_update = datetime.now(timezone.utc)
        
    def create_inventory_movement(self, material_id: int, quantity: float, reference_type: MoveType, reference_id: int | None, created_by_id: int) -> InventoryMovement:
        movement = InventoryMovement(material_id = material_id, 
                                     quantity = quantity, 
                                     reference_type = reference_type, 
                                     reference_id = reference_id, 
                                     created_by_id = created_by_id)
        self.session.add(movement)
        return movement