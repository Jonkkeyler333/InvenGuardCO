from fastapi import APIRouter, Depends, HTTPException, Form, Request
from fastapi.responses import HTMLResponse
from app.core.templating import templates
from app.core.dependencies import DbSession, ClerkOrHigher
from app.core.exceptions import MaterialAlreadyExistsError
from app.services.material_services import create_material, get_all_material
from app.schemas.material_schemas import MaterialCreate

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
                             clerk_user: ClerkOrHigher,
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
                        clerk_user: ClerkOrHigher,
                        page: int = 1,
                        order_by_inventory: bool = False,
                        desc: bool = False,
                        critical_only:  bool = False):
    materials, total_pages = get_all_material(session, page = page, limit = 10,
                                              order_by_inventory = order_by_inventory,
                                              desc = desc,
                                              critical_only = critical_only)
    return templates.TemplateResponse("materials/partials/materials_table.html", 
                                      {"request": request, 
                                       "materials": materials,
                                       "page": page,
                                       "order_by_inventory": order_by_inventory,
                                       "desc": desc,
                                       "critical_only": critical_only,
                                       "total_pages": total_pages})