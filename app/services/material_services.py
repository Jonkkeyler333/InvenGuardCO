from datetime import datetime, timezone
from sqlmodel import Session
from app.repositories.material_repository import MaterialRepository
from app.schemas.material_schemas import MaterialCreate, MaterialRead, MaterialUpdate, MaterialInventoryRead, CreateMovementBase, InventoryMovementRead
from app.core.exceptions import MaterialAlreadyExistsError, MaterialNotFoundError, InsufficientInventoryError, LockInventoryError
from typing import Tuple
from sqlalchemy.exc import OperationalError

def create_material(db: Session, material_create: MaterialCreate) -> MaterialRead:
    repository = MaterialRepository(db)
    if repository.get_material_by_sku(material_create.sku):
        raise MaterialAlreadyExistsError(material_create.sku)
    material = repository.create_material(**material_create.model_dump(exclude_unset = True))
    return MaterialRead.model_validate(material)

def get_all_material(db: Session, page: int = 1,
                     limit: int = 10,
                     order_by_inventory: bool = False,
                     critical_only: bool = False,
                     desc: bool = False) -> Tuple[list[MaterialRead], int]:
    repository = MaterialRepository(db)
    if critical_only:
        materials = repository.get_critical_inventory_materials(desc = desc)
        return [MaterialRead.model_validate(material) for material in materials], 1
    if order_by_inventory:
        materials, total_pages = repository.get_all_material_inventory(page = page , limit = limit, desc = desc)
        return [MaterialRead.model_validate(material) for material in materials], total_pages
    materials, total_pages = repository.get_all_material(page = page , limit = limit)
    return [MaterialRead.model_validate(material) for material in materials], total_pages

def inventory_movement(db: Session, movement: CreateMovementBase) -> InventoryMovementRead:
    repository = MaterialRepository(db)
    try:
        inventory = repository.lock_inventory_row(movement.material_id)
        if inventory is None:
            raise MaterialNotFoundError(movement.material_id)
        new_qty = inventory.quantity_available + movement.quantity if movement.reference_type in ["ENTRY", "ADJUSTMENT_POSITIVE"] else inventory.quantity_available - movement.quantity
        if new_qty < 0:
            raise InsufficientInventoryError(movement.material_id, inventory.quantity_available, movement.quantity)
        inventory.quantity_available = new_qty
        inventory.last_update = datetime.now(timezone.utc)
        movement_db = repository.create_inventory_movement(**movement.model_dump(exclude_unset = True))
        db.commit()
        return InventoryMovementRead.model_validate(movement_db)
    except OperationalError:
        db.rollback()
        raise LockInventoryError(movement.material_id)
    except:
        db.rollback()
        raise ValueError("An error occurred during inventory movement.")