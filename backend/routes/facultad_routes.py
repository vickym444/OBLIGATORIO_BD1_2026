from fastapi import APIRouter, HTTPException
from schemas.facultad_schema import FacultadCreate, FacultadUpdate
from services.facultad_service import facultad_service

router = APIRouter(prefix="/facultades", tags=["facultades"])


@router.get("")
def listar():
    return {"data": facultad_service.listar_facultades()}


@router.get("/{id_facultad}")
def obtener(id_facultad: int):
    facultad = facultad_service.obtener_facultad(id_facultad)
    if not facultad:
        raise HTTPException(status_code=404, detail="Facultad no encontrada")
    return {"data": facultad}


@router.post("")
def crear(data: FacultadCreate):
    try:
        id_nuevo = facultad_service.crear_facultad(data.nombre)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"data": {"id_facultad": id_nuevo}}


@router.put("/{id_facultad}")
def actualizar(id_facultad: int, data: FacultadUpdate):
    try:
        filas = facultad_service.actualizar_facultad(id_facultad, data.nombre, data.activo)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    if not filas:
        raise HTTPException(status_code=404, detail="Facultad no encontrada")
    return {"data": {"actualizado": True}}


@router.delete("/{id_facultad}")
def eliminar(id_facultad: int):
    filas = facultad_service.eliminar_facultad(id_facultad)
    if not filas:
        raise HTTPException(status_code=404, detail="Facultad no encontrada")
    return {"data": {"eliminado": True}}