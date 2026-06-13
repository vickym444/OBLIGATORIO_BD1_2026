from fastapi import APIRouter, HTTPException
from schemas.facultad_schema import FacultadCreate, FacultadUpdate
import services.facultad_service as service

router = APIRouter(prefix="/facultades", tags=["facultades"])


@router.get("")
def listar():
    return {"data": service.listar_facultades()}


@router.get("/{id_facultad}")
def obtener(id_facultad: int):
    facultad = service.obtener_facultad(id_facultad)
    if not facultad:
        raise HTTPException(status_code=404, detail="Facultad no encontrada")
    return {"data": facultad}


@router.post("")
def crear(data: FacultadCreate):
    id_nuevo = service.crear_facultad(data.nombre)
    return {"data": {"id_facultad": id_nuevo}}


@router.put("/{id_facultad}")
def actualizar(id_facultad: int, data: FacultadUpdate):
    filas = service.actualizar_facultad(id_facultad, data.nombre, data.activo)
    if not filas:
        raise HTTPException(status_code=404, detail="Facultad no encontrada")
    return {"data": {"actualizado": True}}


@router.delete("/{id_facultad}")
def eliminar(id_facultad: int):
    filas = service.eliminar_facultad(id_facultad)
    if not filas:
        raise HTTPException(status_code=404, detail="Facultad no encontrada")
    return {"data": {"eliminado": True}}