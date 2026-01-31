from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse, Response
from app.core.templating import templates
from app.core.dependencies import DbSession, ClerkOrHigher
from app.core.exceptions import MaterialAlreadyExistsError, MaterialNotFoundError, InsufficientInventoryError, LockInventoryError, MaterialWithActiveInventoryError
from app.services.material_services import create_material, inactive_material, get_all_material, inventory_movement, get_material_by_id, update_material_thresholds
from app.schemas.material_schemas import MaterialCreate, CreateMovementBase, InventoryMovementRead, MaterialUpdateThresholds
from pydantic import ValidationError

router = APIRouter(prefix="/materials", tags=["materials"])

@router.get("/", response_class = HTMLResponse)
def materials_page(request: Request):
    return templates.TemplateResponse("materials/index.html", {"request": request})

@router.get("/create", response_class = HTMLResponse)
def create_material_page(request: Request):
    return templates.TemplateResponse("materials/register_material.html", {"request": request})

@router.post("/create", response_class = HTMLResponse)
def create_material_endpoint(request: Request,
                             session: DbSession,
                             user: ClerkOrHigher,
                             name: str = Form(), 
                             sku: str = Form(), 
                             unit_measure: str = Form()):
    try:
        data_material = MaterialCreate(name = name, sku = sku, unit_measure = unit_measure)
        material = create_material(session, data_material)
        return templates.TemplateResponse("materials/partials/register_form.html", 
                                          {"request": request, "success": True, 
                                           "message": f" Material {material.sku} created successfully."})
    except MaterialAlreadyExistsError as e:
        return templates.TemplateResponse("materials/partials/register_form.html", 
                                          {"request": request, "error": True, 
                                           "message": str(e)})
        
@router.get("/list", response_class = HTMLResponse)
def list_materials_page(request: Request,
                        session: DbSession,
                        user: ClerkOrHigher,
                        page: int = 1,
                        order_by_inventory: bool = False,
                        desc: bool = False,
                        critical_only:  bool = False,
                        inactive: bool = False):
    materials, total_pages = get_all_material(session, page = page, limit = 10,
                                              order_by_inventory = order_by_inventory,
                                              desc = desc,
                                              critical_only = critical_only,
                                              inactive = inactive)
    return templates.TemplateResponse("materials/partials/materials_table.html", 
                                      {"request": request, 
                                       "materials": materials,
                                       "page": page,
                                       "order_by_inventory": order_by_inventory,
                                       "desc": desc,
                                       "user" : user,
                                       "inactive": inactive,
                                       "critical_only": critical_only,
                                       "total_pages": total_pages})
    
@router.get("/{id}/movement", response_class = HTMLResponse)
def material_movement_page(request: Request,
                           user: ClerkOrHigher,
                           id: int):
    return templates.TemplateResponse("materials/partials/register_movement.html", 
                                      {"request": request,
                                       "material_id": id,
                                       "user" : user})
    
@router.post("/{id}/movement", response_class = HTMLResponse)
def register_material_movement(request: Request,
                               session: DbSession,
                               user: ClerkOrHigher,
                               id: int,
                               quantity: float = Form(),
                               reference_id: int | None = Form(None),
                               reference_type: str = Form()):
    try:
        movevement_data = CreateMovementBase(material_id = id,
                                             quantity = quantity,
                                             created_by_id = user.id,
                                             reference_id = reference_id,
                                             reference_type = reference_type)
        movement = inventory_movement(session, movevement_data)
        return templates.TemplateResponse("materials/partials/register_movement.html", 
                                          {"request": request,
                                           "material_id": id,
                                           "user": user,
                                           "success": f"Inventory movement of {movement.quantity} registered successfully."})
    except ValidationError as e:
        error_messages = []
        for error in e.errors():
            field = error["loc"][0] if error["loc"] else "field"
            msg = error["msg"]
            error_messages.append(f"{field}: {msg}")
        return templates.TemplateResponse(
            "materials/partials/register_movement.html",
            {"request": request,"user": user, "error": " | ".join(error_messages), "material_id": id}
        )
    except (MaterialNotFoundError, InsufficientInventoryError, LockInventoryError) as e:
        return templates.TemplateResponse("materials/partials/register_movement.html", 
                                          {"request": request,
                                           "user": user,  
                                           "error": str(e)})
        
@router.delete("/{id}", response_class = HTMLResponse)
def delete_material_endpoint(request: Request,
                             session: DbSession,
                             user: ClerkOrHigher,
                             id: int):
    try:
        success = inactive_material(session, id)
        if success:
            response = Response(status_code=204)
            response.headers["HX-Trigger"] = 'materialDeleted'
            return response
        else:
            return templates.TemplateResponse("materials/partials/materials_table.html", 
                                          {"request": request, 
                                           "error": "Unexpected error occurred while deleting the material."}) 
    except (MaterialNotFoundError, LockInventoryError, MaterialWithActiveInventoryError) as e:
        return templates.TemplateResponse("materials/partials/materials_table.html", 
                                          {"request": request, 
                                           "error": str(e)})
        
@router.get("/{id}/thresholds", response_class = HTMLResponse)
def material_thresholds_page(request: Request,
                             user: ClerkOrHigher,
                             session: DbSession,
                             id: int):
    try:
        material = get_material_by_id(session, id)
        return templates.TemplateResponse("materials/partials/update_thresholds.html",
                                          {"request": request,
                                           "material": material,
                                           "user" : user})
    except MaterialNotFoundError as e:
        return templates.TemplateResponse("materials/partials/update_thresholds.html", 
                                          {"request": request,
                                           "error": str(e),
                                           "user" : user})
        
@router.post("/{id}/thresholds", response_class = HTMLResponse)
def update_material_thresholds_endpoint(request: Request,
                                        session: DbSession,
                                        user: ClerkOrHigher,
                                        id: int,
                                        reorder_threshold: float = Form(),
                                        critical_threshold: float = Form()):
    
    material_db = get_material_by_id(session, id)
    if not material_db:
        return templates.TemplateResponse("materials/partials/update_thresholds.html", 
                                          {"request": request,
                                           "error": f"Material with ID {id} not found.",
                                           "user" : user})
    try:
        update_data = MaterialUpdateThresholds(material_id = id, reorder_threshold = reorder_threshold, critical_threshold = critical_threshold)
        material = update_material_thresholds(session, update_data)
        return templates.TemplateResponse("materials/partials/update_thresholds.html",
                                          {"request": request,
                                           "material": material,
                                           "user" : user,
                                           "success": f"Thresholds updated successfully for material {material.sku}."})
    except ValidationError as e:
        error_messages = []
        for error in e.errors():
            field = error["loc"][0] if error["loc"] else "field"
            msg = error["msg"]
            error_messages.append(f"{field}: {msg}")
        return templates.TemplateResponse(
            "materials/partials/update_thresholds.html",
            {"request": request,"material":material_db, "user": user, "error": " | ".join(error_messages)}
        )
    except LockInventoryError as e:
        return templates.TemplateResponse("materials/partials/update_thresholds.html", 
                                          {"request": request,
                                           "error": str(e),
                                           "material": material_db,
                                           "user" : user})
    except MaterialNotFoundError as e:
        return templates.TemplateResponse("materials/partials/update_thresholds.html", 
                                          {"request": request,
                                           "error": str(e),
                                           "material": material_db,
                                           "user" : user})
        
@router.get("/{id}/edit", response_class = HTMLResponse)
def edit_material_page(request: Request,
                       user: ClerkOrHigher,
                       session: DbSession,
                       id: int):
    try:
        material = get_material_by_id(session, id)
        return templates.TemplateResponse("materials/partials/edit_material.html",
                                          {"request": request,
                                           "material": material,
                                           "user" : user})
    except MaterialNotFoundError as e:
        return templates.TemplateResponse("materials/partials/edit_material.html", 
                                          {"request": request,
                                           "error": str(e),
                                           "user" : user})