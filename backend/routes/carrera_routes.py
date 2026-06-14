from fastapi import APIRouter, Depends, HTTPException
from core.auth_dependencies import require_admin
from schemas.carrera_schema import CarreraCreate, CarreraUpdate
from services.carrera_service import carrera_service

router = APIRouter(prefix="/carreras", tags=["carreras"])


@router.get("")
def listar(_=Depends(require_admin)):
    return {"data": carrera_service.listar_carreras()}


@router.get("/{id_carrera}")
def obtener(id_carrera: int, _=Depends(require_admin)):
    carrera = carrera_service.obtener_carrera(id_carrera)
    if not carrera:
        raise HTTPException(status_code=404, detail="Carrera no encontrada")
    return {"data": carrera}


@router.post("")
def crear(data: CarreraCreate, _=Depends(require_admin)):
    id_nuevo = carrera_service.crear_carrera(data.nombre, data.id_facultad)
    return {"data": {"id_carrera": id_nuevo}}


@router.put("/{id_carrera}")
def actualizar(id_carrera: int, data: CarreraUpdate, _=Depends(require_admin)):
    filas = carrera_service.actualizar_carrera(
        id_carrera, data.nombre, data.id_facultad, data.activo
    )
    if not filas:
        raise HTTPException(status_code=404, detail="Carrera no encontrada")
    return {"data": {"actualizado": True}}


@router.delete("/{id_carrera}")
def eliminar(id_carrera: int, _=Depends(require_admin)):
    filas = carrera_service.eliminar_carrera(id_carrera)
    if not filas:
        raise HTTPException(status_code=404, detail="Carrera no encontrada")
    return {"data": {"eliminado": True}}