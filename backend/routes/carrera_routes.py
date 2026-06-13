from fastapi import APIRouter, HTTPException
from schemas.carrera_schema import CarreraCreate, CarreraUpdate
import services.carrera_service as service

router = APIRouter(prefix="/carreras", tags=["carreras"])


@router.get("")
def listar():
    return {"data": service.listar_carreras()}


@router.get("/{id_carrera}")
def obtener(id_carrera: int):
    carrera = service.obtener_carrera(id_carrera)
    if not carrera:
        raise HTTPException(status_code=404, detail="Carrera no encontrada")
    return {"data": carrera}


@router.post("")
def crear(data: CarreraCreate):
    id_nuevo = service.crear_carrera(data.nombre, data.id_facultad)
    return {"data": {"id_carrera": id_nuevo}}


@router.put("/{id_carrera}")
def actualizar(id_carrera: int, data: CarreraUpdate):
    filas = service.actualizar_carrera(
        id_carrera, data.nombre, data.id_facultad, data.activo
    )
    if not filas:
        raise HTTPException(status_code=404, detail="Carrera no encontrada")
    return {"data": {"actualizado": True}}


@router.delete("/{id_carrera}")
def eliminar(id_carrera: int):
    filas = service.eliminar_carrera(id_carrera)
    if not filas:
        raise HTTPException(status_code=404, detail="Carrera no encontrada")
    return {"data": {"eliminado": True}}